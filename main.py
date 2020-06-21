# This script controls the virtualbox

# System
import sys
import logging
from pathlib import Path
from os import path

# Modules
from MyModules import PackagesExporter
from MyModules import PackagesImporter
from MyModules import Configuration
from MyModules import ArgsReader
from MyModules import MyGlobals

main_script_path = str(path.abspath(__file__))
main_script_dir = str((Path(main_script_path)).parent)


def log_info(msg=""):
    logging.getLogger(__name__).info(msg)


def log_debug(msg=""):
    logging.getLogger(__name__).debug(msg)


def log_error(msg=""):
    logging.getLogger(__name__).error(msg)


def check_min_supported_python_version():
    if sys.version_info[0] < 3:
        print("Python 3 or a more recent version is required.")
        MyGlobals.terminate_program(1)


def configure_console_logger():
    logging.getLogger().setLevel(logging.INFO)
    format_str = Configuration.log_fmt_str
    formatter = logging.Formatter(format_str, datefmt=Configuration.log_time_fmt)

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)


def add_log_file_logging():
    try:
        log_debug("Logging to file: {}".format(Configuration.log_file))
        format_str = Configuration.log_fmt_str
        formatter = logging.Formatter(format_str, datefmt=Configuration.log_file_time_fmt)

        f_handler = logging.FileHandler(Configuration.log_file, mode='w')
        f_handler.setLevel(logging.INFO)
        f_handler.setFormatter(formatter)
        logging.getLogger().addHandler(f_handler)
    except BaseException as error_msg:
        log_error("Failed logging to file at: {}\n{}\nAborting..".format(Configuration.log_file, error_msg))
        MyGlobals.terminate_program(1)


def log_summary():
    if Configuration.export_packages:
        PackagesExporter.log_failed_to_export_summary()
    if Configuration.import_packages:
        PackagesImporter.log_failed_to_import_summary()


def main():
    check_min_supported_python_version()

    configure_console_logger()  # Default logs: to console

    # Handle args:
    args = sys.argv[1:]
    ArgsReader.read_args(args)

    # Init
    Configuration.initialize_app(main_script_dir, main_script_path)

    # Check if need to log to file as well
    if Configuration.log_file and len(logging.getLogger().handlers) < 2:  # Only two handlers are supported - Console & Log File
        add_log_file_logging()

    # Main dish
    if Configuration.export_packages:
        PackagesExporter.export_packages()
    if Configuration.import_packages:
        PackagesImporter.import_packages()

    # Print nice summary
    log_summary()

    # Finish successfully
    MyGlobals.terminate_program(0)


# Start
main()



