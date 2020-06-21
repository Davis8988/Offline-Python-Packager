# This module contains import python packages functions

# System
import os.path
import logging
from tabulate import tabulate

# Modules
from MyModules import MyGlobals
from MyModules import Configuration
from MyModules.PythonPackge import PyPackage

packages_to_import = {}


def import_packages():
    import_list = Configuration.import_packages.split(',')
    for packages_src in import_list:
        collect_packages_to_import(packages_src.strip())
    print_packages_to_import_dict()
    import_collected_packages()


def collect_packages_to_import(packages_src):
    if not packages_src:
        log_warning("Skipping import of null or empty string value")
        return

    if MyGlobals.is_file(packages_src):
        log_debug("Reading packages from file: {}".format(packages_src))
        action_dict = MyGlobals.read_file_lines_as_list(packages_src)
        if not action_dict["Result"]:
            MyGlobals.terminate_program(1)
        packages_list = action_dict["MoreInfo"]
        add_packages_list_to_packages_to_import_dict(packages_list)
    elif packages_src == "*":
        add_all_pip_available_packages_to_packages_to_import_dict()
    else:
        add_package_to_packages_to_import_dict(packages_src)  # Normal package request:  'pkg_name' or 'pkg_name==pkg_version'


def add_packages_list_to_packages_to_import_dict(packages_list):
    for pkg in packages_list:
        add_package_to_packages_to_import_dict(pkg)


def add_package_to_packages_to_import_dict(pkg_str):
    global packages_to_import
    pkg_str = str(pkg_str).strip().lower()
    pkg_arr = [pkg_str, None]
    if "==" in pkg_str:
        pkg_arr = [x.strip() for x in pkg_str.split("==")]
    pkg_name = pkg_arr[0]
    pkg_version = pkg_arr[1]
    py_pkg = PyPackage(pkg_name, pkg_version)
    packages_to_import[pkg_name] = py_pkg


def print_packages_to_import_dict():
    packages_to_import_str = get_all_packages_to_import_oneline()
    log_info("Importing packages:\n{}\nfrom: {}\n".format(packages_to_import_str, Configuration.import_from))


def get_all_packages_to_import_oneline():
    return ", ".join(packages_to_import.keys())


def import_collected_packages():
    for pkg_name, py_pkg in packages_to_import.items():
        import_result = import_package(py_pkg)
        if import_result["Result"]:
            py_pkg.imported = True
            log_info("Successfully imported {}".format(py_pkg.full_name))
        else:
            err_msg = import_result["MoreInfo"].output.decode(Configuration.decode_commands_output_fmt)
            py_pkg.more_info = err_msg
            log_error(err_msg)


def import_package(py_pkg):
    import_msg = "Importing package: {}".format(py_pkg.full_name)
    log_info(import_msg)

    pip = Configuration.pip_executable
    # import_opts = "install --no-index --find-links=\"{}\" {}".format(Configuration.import_from, py_pkg.full_name)
    index_url = Configuration.index_url
    if os.name == 'nt':
        index_url = "file:///{}".format(index_url)
    import_opts = "install --index-url=\"{}\" {}".format(index_url, py_pkg.full_name)
    extra_pip_args = Configuration.extra_pip_args
    cmnd = "{} {} {}".format(pip, import_opts, extra_pip_args)
    return MyGlobals.execute_command(cmnd)


def add_all_pip_available_packages_to_packages_to_import_dict():
    simple_index_dir = Configuration.simple_index_dir
    if MyGlobals.dir_exists(simple_index_dir):
        dir_flat_files_list = os.listdir(simple_index_dir)
    else:
        dir_flat_files_list = os.listdir(Configuration.import_from)
        dir_flat_files_list = convert_flat_files_names_list_to_packages_names(dir_flat_files_list)

    for pkg_name in dir_flat_files_list:
        if pkg_name.lower() == "index.html":
            continue
        add_package_to_packages_to_import_dict(pkg_name)


def convert_flat_files_names_list_to_packages_names(dir_flat_files_list):
    pkgs_names_list = []
    for file_name in dir_flat_files_list:
        if "-" not in file_name:
            pkg_name = file_name
        else:
            file_name_arr = file_name.split("-")
            pkg_name = file_name_arr[0].strip()
        pkgs_names_list.append(pkg_name)
    return pkgs_names_list


def get_failed_import_packages_table():
    headers = ["Package", "Imported", "Error"]
    table = []
    for pkg_name, py_pkg in packages_to_import.items():
        if not py_pkg.imported:
            table.append([py_pkg.full_name, False, py_pkg.more_info])
    if len(table) == 0:
        return None
    return tabulate(table, headers=headers)


def log_failed_to_import_summary():
    failed_import_table = get_failed_import_packages_table()
    if failed_import_table is None:
        packages_to_import_str = get_all_packages_to_import_oneline()
        log_info("Successfully imported all packages: \n{}".format(packages_to_import_str))
    else:
        log_info("\nFailed to Import Summary:\n{}".format(failed_import_table))


def log_info(msg=""):
    logging.getLogger(__name__).info(msg)


def log_debug(msg=""):
    logging.getLogger(__name__).debug(msg)


def log_warning(msg=""):
    logging.getLogger(__name__).warning(msg)


def log_error(msg=""):
    logging.getLogger(__name__).error(msg)

