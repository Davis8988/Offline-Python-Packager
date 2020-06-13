# This module contains export python packages functions

# System
import logging
import time
from datetime import timedelta

# Modules
from MyModules import MyGlobals
from MyModules import Configuration
from MyModules.PythonPackge import PyPackage

packages_to_export = []


def export_packages():
    export_list = Configuration.export_packages.split(',')
    for packages_src in export_list:
        collect_packages_to_export(packages_src.strip())
    print_packages_to_export_dict()
    export_collected_packages()


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
    packages_to_export.append(py_pkg)


def print_packages_to_export_dict():
    packages_to_export_str = ''
    for py_pkg in packages_to_export:
        packages_to_export_str += "{}\n".format(py_pkg.full_name)
    log_info("Exporting packages:\n{}".format(packages_to_export_str))


def export_collected_packages():
    for py_pkg in packages_to_export:
        export_package(py_pkg)


def export_package(py_pkg):
    pkg_name = py_pkg.name
    pkg_version = py_pkg.version
    export_msg = "Exporting package: {}".format(py_pkg.full_name)
    log_info(export_msg)

    export_cmnd = "pip download -d \"{}\" {}".format(Configuration.export_to, py_pkg.full_name)
    export_result = MyGlobals.execute_command(export_cmnd)
    if export_result["Result"]:
        log_info("Successfully downloaded {}".format(py_pkg.full_name))
        py_pkg.exported = True
    else:
        log_error(export_result["MoreInfo"].output.decode("utf-8"))


def log_info(msg=""):
    logging.getLogger(__name__).info(msg)


def log_debug(msg=""):
    logging.getLogger(__name__).debug(msg)


def log_warning(msg=""):
    logging.getLogger(__name__).warning(msg)


def log_error(msg=""):
    logging.getLogger(__name__).error(msg)

