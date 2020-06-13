# This module contains export python packages functions

# System
import logging
import time
from datetime import timedelta

# Modules
from MyModules import MyGlobals
from MyModules import Configuration

packages_to_export = {}


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


def add_package_to_packages_to_export_dict(pkg):
    global packages_to_export
    pkg = str(pkg).strip().lower()
    pkg_arr = [pkg, None]
    if "==" in pkg:
        pkg_arr = [x.strip() for x in pkg.split("==")]
    pkg_name = pkg_arr[0]
    pkg_version = pkg_arr[1]
    packages_to_export[pkg_name] = pkg_version


def print_packages_to_export_dict():
    packages_to_export_str = ''
    for k, v in packages_to_export.items():
        packages_to_export_str += "{}".format(k)
        if v:
            packages_to_export_str += "=={}".format(v)
        packages_to_export_str += "\n"
    log_info("Exporting packages:\n{}".format(packages_to_export_str))


def export_collected_packages():
    for pkg_name, pkg_version in packages_to_export.items():
        export_package(pkg_name, pkg_version)


def export_package(pkg_name, pkg_version):
    export_msg = "Exporting package: pkg_name"
    export_msg += "=={}".format(pkg_version) if pkg_version else export_msg
    log_info(export_msg)

    export_cmnd = "pip download -d \"{}\" {}".format(Configuration.export_to, pkg_name)
    export_cmnd += "=={}".format(pkg_version) if pkg_version else export_cmnd
    MyGlobals.execute_command(export_cmnd)




def log_info(msg=""):
    logging.getLogger(__name__).info(msg)


def log_debug(msg=""):
    logging.getLogger(__name__).debug(msg)


def log_warning(msg=""):
    logging.getLogger(__name__).warning(msg)


def log_error(msg=""):
    logging.getLogger(__name__).error(msg)

