# This module contains configurations to be used by other scripts

from datetime import datetime
import logging
import os

log_file = None
log_level = None
log_fmt = '%(asctime)s [%(levelname)-5s] %(threadName)s: %(message)s'
is_verbose = False

date_today = datetime.now()


def initialize_app(main_script_dir, main_script_path):
    log_info("Initializing..")
    define_app_special_envs(main_script_dir, main_script_path)


def define_app_special_envs(main_script_dir, main_script_path):
    log_debug("Defining special app envs: OFFLINE_PYTHON_PACKAGER_HOME, OFFLINE_PYTHON_PACKAGER_EXECUTABLE")
    dockerized_installer_home = main_script_dir
    dockerized_installer_executable = main_script_path
    os.environ["OFFLINE_PYTHON_PACKAGER_HOME"] = str(dockerized_installer_home)
    os.environ["OFFLINE_PYTHON_PACKAGER_EXECUTABLE"] = str(dockerized_installer_executable)


def log_info(msg=""):
    logging.getLogger(__name__).info(msg)


def log_debug(msg=""):
    logging.getLogger(__name__).debug(msg)


def log_error(msg=""):
    logging.getLogger(__name__).error(msg)