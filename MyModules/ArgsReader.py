# This module contains function to read cmd arguments

# System
import argparse
import logging
import sys

# Modules
from MyModules import Configuration

parser = argparse.ArgumentParser(description='Offline Exporter & Importer for python packages')
parser.add_argument("-ep", "--export_pacakges", dest="export", help="Export python packages", action='store_false')
parser.add_argument("-ip", "--import_pacakges", dest="import", help="Import python packages", action='store_false')
parser.add_argument("-l", "--log_file", help="File path to write logs to")
parser.add_argument("-v", "--verbose", help="More awsome printings.", action='store_false')

received_args = None


def read_args(args_list):
    log_info("Reading args: {}".format(args_list))
    global received_args
    try:
        received_args = parser.parse_args()
    except SystemExit as errorCode:
        sys.exit(errorCode)
    except BaseException as errorMsg:
        log_error("Error - Failed to parse args: {}\n{}".format(args_list, errorMsg))
        return False
    if received_args.conf_file:
        Configuration.conf_file_path = received_args.conf_file
    if received_args.verbose:
        Configuration.is_verbose = received_args.verbose
    # if parsed_args.tasks_names:
    #     Configuration.tasks_names_to_execute = get_tasks_names_list(parsed_args.tasks_names)
    if received_args.log_file:
        Configuration.log_file = received_args.log_file

    log_debug("Finished reading args successfully")
    return True


# def get_tasks_names_list(tasks_names_str):
    # return [x.strip() for x in str(tasks_names_str).split(",")]


def log_info(msg=""):
    logging.getLogger(__name__).info(msg)


def log_debug(msg=""):
    logging.getLogger(__name__).debug(msg)


def log_error(msg=""):
    logging.getLogger(__name__).error(msg)

