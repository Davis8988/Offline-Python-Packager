# This module contains export python packages functions

# System
import logging
from os import path
from tabulate import tabulate

# Modules
from MyModules import MyGlobals
from MyModules import MyDir2Pi
from MyModules import Configuration
from MyModules.PythonPackge import PyPackage

packages_to_export = {}
exported_packages_files_data = {}
last_exported_dir_files = None


def export_packages():
    export_list = Configuration.export_packages.split(',')
    for packages_src in export_list:
        collect_packages_to_export(packages_src.strip())

    print_packages_to_export_dict()

    # Export the packages to: Configuration.export_to
    export_collected_packages()

    if not MyGlobals.is_dir(Configuration.export_to):
        log_error("Finish exporting but missing exported packages dir: {}\nSomething went wrong. Check log above.".format(Configuration.export_to))
        MyGlobals.terminate_program(1)
    MyDir2Pi.index_packages_dir(Configuration.export_to)
    # log_debug("Writing exported packages files data to: {}".format(Configuration.exported_files_json_file))
    # MyGlobals.write_json_file(exported_packages_files_data, Configuration.exported_files_json_file)


def collect_packages_to_export(packages_src):
    if not packages_src:
        log_warning("Skipping export of null or empty string value")
        return

    if MyGlobals.is_file(packages_src):
        log_debug("Reading packages from file: {}".format(packages_src))
        action_dict = MyGlobals.read_file_lines_as_list(packages_src)
        if not action_dict["Result"]:
            MyGlobals.terminate_program(1)
        packages_list = action_dict["MoreInfo"]
        add_packages_list_to_packages_to_export_dict(packages_list)
    elif packages_src == "*":
        add_all_pip_freeze_packages_to_packages_to_export_dict()
    else:
        add_package_to_packages_to_export_dict(packages_src)  # Normal package request:  'pkg_name' or 'pkg_name==pkg_version'


def add_packages_list_to_packages_to_export_dict(packages_list):
    for pkg in packages_list:
        add_package_to_packages_to_export_dict(pkg)


def add_package_to_packages_to_export_dict(pkg_str):
    global packages_to_export
    pkg_str = str(pkg_str).strip().lower()
    pkg_arr = [pkg_str, None]
    if "==" in pkg_str:
        pkg_arr = [x.strip() for x in pkg_str.split("==")]
    pkg_name = pkg_arr[0]
    pkg_version = pkg_arr[1]
    py_pkg = PyPackage(pkg_name, pkg_version)
    packages_to_export[pkg_name] = py_pkg


def print_packages_to_export_dict():
    packages_to_export_str = get_all_packages_to_export_oneline()
    log_info("Exporting packages:\n{}\nto: {}\n".format(packages_to_export_str, Configuration.export_to))


def get_all_packages_to_export_oneline():
    return ", ".join(packages_to_export.keys())


def export_collected_packages():
    for pkg_name, py_pkg in packages_to_export.items():
        export_result = export_package(py_pkg)
        if export_result["Result"]:
            py_pkg.exported = True
            # register_exported_files(py_pkg)
            log_info("Successfully downloaded {}".format(py_pkg.full_name))
        else:
            py_pkg.exported = True
            log_info("Successfully downloaded {}".format(py_pkg.full_name))


def export_package(py_pkg):
    export_msg = "Exporting package: {}".format(py_pkg.full_name)
    log_info(export_msg)

    pip = Configuration.pip_executable
    import_opts = "download -d \"{}\" {}".format(Configuration.export_to, py_pkg.full_name)
    extra_pip_args = Configuration.extra_pip_args
    cmnd = "{} {} {}".format(pip, import_opts, extra_pip_args)
    return MyGlobals.execute_command(cmnd)


def register_exported_files(py_pkg):
    global last_exported_dir_files
    exported_packags_path = path.join(Configuration.export_to, "*.*")
    current_exported_dir_files = MyGlobals.get_files_list_from_path(exported_packags_path)
    new_created_files = MyGlobals.list_subtract(current_exported_dir_files, last_exported_dir_files)
    log_info("Newly created files: {}".format(new_created_files))
    exported_packages_files_data[py_pkg.name] = new_created_files
    last_exported_dir_files = current_exported_dir_files


def add_all_pip_freeze_packages_to_packages_to_export_dict():
    pip = Configuration.pip_executable
    opts = "freeze"
    cmnd = "{} {}".format(pip, opts)
    action_dict = MyGlobals.execute_command(cmnd)
    if not action_dict["Result"]:
        log_error("Failed to retrieve all installed pip packages using 'pip freeze' command")
        MyGlobals.terminate_program(1)
    pip_freeze_output = action_dict["MoreInfo"].decode(Configuration.decode_commands_output_fmt).split("\n")
    for pkg_str in pip_freeze_output:
        if pkg_str and "==" not in pkg_str:
            log_warning("pip freeze command invalid output: {}. Not in format of: pkg_name==pkg_version. Skipping this line".format(pkg_str))
            continue
        add_package_to_packages_to_export_dict(pkg_str)


def get_failed_export_packages_table():
    headers = ["Package", "Exported", "Error"]
    table = []
    for pkg_name, py_pkg in packages_to_export.items():
        if not py_pkg.exported:
            table.append([py_pkg.full_name, False, py_pkg.more_info])
    if len(table) == 0:
        return None
    return tabulate(table, headers=headers)


def log_failed_to_export_summary():
    failed_export_table = get_failed_export_packages_table()
    if failed_export_table is None:
        packages_to_export_str = get_all_packages_to_export_oneline()
        log_info("Successfully exported all packages: \n{}".format(packages_to_export_str))
    else:
        log_info("\nFailed to Export Summary:\n{}".format(failed_export_table))



def log_info(msg=""):
    logging.getLogger(__name__).info(msg)


def log_debug(msg=""):
    logging.getLogger(__name__).debug(msg)


def log_warning(msg=""):
    logging.getLogger(__name__).warning(msg)


def log_error(msg=""):
    logging.getLogger(__name__).error(msg)

