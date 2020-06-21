# This module contains configurations to be used by other scripts

# System
from datetime import datetime
import logging
import os
import sys

# Modules
from MyModules import MyGlobals

log_file = "${OFFLINE_PYTHON_PACKAGER_HOME}\\offline-python-packager.log"
log_level = None
# log_fmt = '%(asctime)s [%(levelname)-5s] %(threadName)s: %(message)s'
log_fmt_str = '%(asctime)s [%(levelname)-5s] : %(message)s'
log_time_fmt = "%H:%M:%S"
log_file_time_fmt = "%Y-%m-%d %H:%M:%S"
is_verbose = False

pip_executable = "python3 -m pip"  # Linux
if os.name == 'nt':
    pip_executable = "python -m pip"   # Windows

extra_pip_args = ""
exported_packages_dir_name = "exported_packages"
export_packages = None
export_to = os.path.join("${OFFLINE_PYTHON_PACKAGER_HOME}", exported_packages_dir_name)
import_packages = None
import_from = os.path.join("${OFFLINE_PYTHON_PACKAGER_HOME}", exported_packages_dir_name)
exported_files_json_file = os.path.join(export_to, "simple", "exported_files.json")

# Packages Index
simple_index_dir = None
index_url = None

date_today = datetime.now()

decode_commands_output_fmt = "utf-8"
json_file_data_fmt = "utf-8"


def initialize_app(main_script_dir, main_script_path):
    log_info("Initializing..")
    define_app_special_envs(main_script_dir, main_script_path)
    init()


def define_app_special_envs(main_script_dir, main_script_path):
    log_debug("Defining special app envs: OFFLINE_PYTHON_PACKAGER_HOME, OFFLINE_PYTHON_PACKAGER_EXECUTABLE")
    os.environ["OFFLINE_PYTHON_PACKAGER_HOME"] = str(main_script_dir)
    os.environ["OFFLINE_PYTHON_PACKAGER_EXECUTABLE"] = str(main_script_path)


def init():
    global pip_executable
    global extra_pip_args
    global pip_2_tgz_executable
    global dir_2_pi_executable
    global export_packages
    global export_to
    global import_packages
    global import_from
    global exported_files_json_file
    global log_file

    global simple_index_dir
    global index_url

    # Expand env variables if any
    pip_executable = MyGlobals.remove_surrounding_quotes(MyGlobals.expand_variable(pip_executable)).strip() if pip_executable else pip_executable
    extra_pip_args = MyGlobals.remove_surrounding_quotes(MyGlobals.expand_variable(extra_pip_args)).strip() if extra_pip_args else extra_pip_args
    export_packages = MyGlobals.remove_surrounding_quotes(MyGlobals.expand_variable(export_packages)).strip() if export_packages else export_packages
    export_to = MyGlobals.remove_surrounding_quotes(MyGlobals.expand_variable(export_to)).strip() if export_to else export_to
    import_packages = MyGlobals.remove_surrounding_quotes(MyGlobals.expand_variable(import_packages)).strip() if import_packages else import_packages
    import_from = MyGlobals.remove_surrounding_quotes(MyGlobals.expand_variable(import_from)).strip() if import_from else import_from
    exported_files_json_file = MyGlobals.remove_surrounding_quotes(MyGlobals.expand_variable(exported_files_json_file)).strip() if exported_files_json_file else exported_files_json_file
    log_file = MyGlobals.remove_surrounding_quotes(MyGlobals.expand_variable(log_file)).strip() if log_file else log_file

    simple_index_dir = os.path.join(import_from, "simple")
    if MyGlobals.dir_exists(simple_index_dir):
        simple_index_dir = MyGlobals.convert_windows_path_to_linux(simple_index_dir)
    index_url = simple_index_dir

    if is_verbose:
        logging.getLogger().setLevel(logging.NOTSET)
        for log_hdnlr in logging.getLogger().handlers:
            log_hdnlr.setLevel(logging.NOTSET)


def log_info(msg=""):
    logging.getLogger(__name__).info(msg)


def log_debug(msg=""):
    logging.getLogger(__name__).debug(msg)


def log_error(msg=""):
    logging.getLogger(__name__).error(msg)