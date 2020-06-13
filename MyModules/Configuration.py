# This module contains configurations to be used by other scripts

from datetime import datetime
import logging
import os

# Modules
from MyModules import MyGlobals

log_file = None
log_level = None
# log_fmt = '%(asctime)s [%(levelname)-5s] %(threadName)s: %(message)s'
log_fmt = '%(asctime)s [%(levelname)-5s] : %(message)s'
is_verbose = False

export_packages = None
export_to = None
import_packages = None
import_from = None
import_to = None

date_today = datetime.now()


def initialize_app(main_script_dir, main_script_path):
    log_info("Initializing..")
    define_app_special_envs(main_script_dir, main_script_path)
    init()


def define_app_special_envs(main_script_dir, main_script_path):
    log_debug("Defining special app envs: OFFLINE_PYTHON_PACKAGER_HOME, OFFLINE_PYTHON_PACKAGER_EXECUTABLE")
    dockerized_installer_home = main_script_dir
    dockerized_installer_executable = main_script_path
    os.environ["OFFLINE_PYTHON_PACKAGER_HOME"] = str(dockerized_installer_home)
    os.environ["OFFLINE_PYTHON_PACKAGER_EXECUTABLE"] = str(dockerized_installer_executable)


def init():
    global export_packages
    global export_to
    global import_packages
    global import_from
    global import_to
    global log_file

    # Expand env variables if any
    export_packages = MyGlobals.remove_surrounding_quotes(MyGlobals.expand_variable(export_packages)).strip()
    export_to = MyGlobals.remove_surrounding_quotes(MyGlobals.expand_variable(export_to)).strip()
    import_packages = MyGlobals.remove_surrounding_quotes(MyGlobals.expand_variable(import_packages)).strip()
    import_from = MyGlobals.remove_surrounding_quotes(MyGlobals.expand_variable(import_from)).strip()
    import_to = MyGlobals.remove_surrounding_quotes(MyGlobals.expand_variable(import_to)).strip()
    log_file = MyGlobals.remove_surrounding_quotes(MyGlobals.expand_variable(log_file)).strip()


def log_info(msg=""):
    logging.getLogger(__name__).info(msg)


def log_debug(msg=""):
    logging.getLogger(__name__).debug(msg)


def log_error(msg=""):
    logging.getLogger(__name__).error(msg)