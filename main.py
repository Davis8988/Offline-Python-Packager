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


def configure_console_logger():
    logging.getLogger().setLevel(logging.NOTSET)
    format_str = Configuration.log_date_fmt
    formatter = logging.Formatter(format_str)

    console = logging.StreamHandler()
    console.setLevel(logging.NOTSET)
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)


def add_log_file_logging():
    log_debug("Logging to file: {}".format(Configuration.log_file))
    format_str = Configuration.log_date_fmt
    formatter = logging.Formatter(format_str, datefmt=Configuration.log_date_fmt)

    f_handler = logging.FileHandler(Configuration.log_file, mode='w')
    f_handler.setLevel(logging.NOTSET)
    f_handler.setFormatter(formatter)
    logging.getLogger().addHandler(f_handler)


def main():
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
    if ArgsReader.received_args.get("export", None):
        PackagesExporter.exportPackages()
    if ArgsReader.received_args.get("import", None):
        PackagesImporter.importPackages()

    # Finish successfully
    MyGlobals.terminateProgram(0)


# Start
main()



