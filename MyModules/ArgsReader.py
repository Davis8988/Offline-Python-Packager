# This module contains function to read cmd arguments

# System
import argparse
import logging
import sys

# Modules
from MyModules import Configuration
from MyModules import MyGlobals

parser = argparse.ArgumentParser(description='Offline Exporter & Importer for python packages')
parser.add_argument("-ep", "--export_pacakges", dest="export_packages", help='Export packages that match pattern. Pass "*" for exporting all packages', nargs='?', default=None, const="*")
parser.add_argument("-et", "--export_to", dest="export_to", help="Export packages to this path", nargs='?', default="${OFFLINE_PYTHON_PACKAGER_HOME}\\exported_packages", const="${OFFLINE_PYTHON_PACKAGER_HOME}\\exported_packages")
parser.add_argument("-ip", "--import_pacakges", dest="import_packages", help='Import packages that match pattern. Pass "*" for importing all packages', nargs='?', default=None, const="*")
parser.add_argument("-if", "--import_from", dest="import_from", help='Import python packages from this path', nargs='?', default="${OFFLINE_PYTHON_PACKAGER_HOME}\\exported_packages", const="${OFFLINE_PYTHON_PACKAGER_HOME}\\exported_packages")
parser.add_argument("-it", "--import_to", dest="import_to", help='Import python packages to this path', nargs='?', default=None, const=None)
parser.add_argument("-l", "--log_file", help="File path to write logs to", nargs='?', default=None, const=None,)
parser.add_argument("-v", "--verbose", help="More awsome printings.", action='store_false')

received_args = None


def read_args(args_list):
    log_info("Reading received args: {}".format(args_list))
    global received_args

    try:
        received_args = parser.parse_args()
    except SystemExit as errorCode:
        MyGlobals.terminateProgram(errorCode)
    except BaseException as errorMsg:
        log_error("Error - Failed to parse received args: {}\n{}".format(args_list, errorMsg))
        MyGlobals.terminateProgram(1)

    Configuration.is_verbose = received_args.verbose
    Configuration.export_packages = received_args.export_packages
    Configuration.import_packages = received_args.import_packages
    Configuration.log_file = received_args.log_file

    log_debug("Finished reading args successfully")


def log_info(msg=""):
    logging.getLogger(__name__).info(msg)


def log_debug(msg=""):
    logging.getLogger(__name__).debug(msg)


def log_error(msg=""):
    logging.getLogger(__name__).error(msg)

