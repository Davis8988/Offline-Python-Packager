# This module contains function to read cmd arguments

# System
import argparse
import logging
import sys
from os import path

# Modules
from MyModules import Configuration
from MyModules import MyGlobals


class MyArgsParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


def get_execution_examples():
    examples_str = [
        ' Export:',
        '  * Export all local packages to default location: \"python main.py -ep\"',
        '  * Export all local packages to location: \"python main.py -ep -et C:\dist\my-packages\"',
        '  * Export specific packages: \"python main.py -ep "pywin32==227, pefile==2019.4.18, ${OFFLINE_PYTHON_PACKAGER_HOME}\packages.txt" -et "C:\dist\my-packages"\"',
        '  * Export with logging to file: \"python main.py -ep "pywin32==227, pefile==2019.4.18, ${OFFLINE_PYTHON_PACKAGER_HOME}\packages.txt" -et "C:\dist\my-packages" -l "${OFFLINE_PYTHON_PACKAGER_HOME}\MyLog.log"\"',
        '',
        ' Import:',
        '  * Import all from default location: \"python main.py -ip\"',
        '  * Import all from location: \"python main.py -ip -if "C:\dist\my-packages"\"',
        '  * Import specific packages: \"python main.py -ip "pywin32==227, pefile==2019.4.18, ${OFFLINE_PYTHON_PACKAGER_HOME}\packages.txt" -if "C:\dist\my-packages"\"',
        '  * Import with logging to file: \"python main.py -ip "pywin32==227, pefile==2019.4.18, ${OFFLINE_PYTHON_PACKAGER_HOME}\packages.txt" -if "C:\dist\my-packages" -l "${OFFLINE_PYTHON_PACKAGER_HOME}\MyLog.log"\"'
    ]

    return "\n".join(examples_str)


parser = MyArgsParser(description='Offline Exporter & Importer for python packages', formatter_class=argparse.RawTextHelpFormatter, epilog="Examples:\n{}".format(get_execution_examples()) )
parser.add_argument("-ep", "--export_packages", dest="export_packages", help='Export packages that match pattern. Pass "*" for exporting all packages', nargs='?', default=None, const="*")
parser.add_argument("-et", "--export_to", dest="export_to", help="Export packages to this path", nargs='?', default=Configuration.export_to, const=Configuration.export_to)
parser.add_argument("-ip", "--import_packages", dest="import_packages", help='Import packages that match pattern. Pass "*" for importing all packages', nargs='?', default=None, const="*")
parser.add_argument("-if", "--import_from", dest="import_from", help='Import python packages from this path', nargs='?', default=Configuration.import_from, const=Configuration.import_from)
parser.add_argument("-pip", "--pip_executable", dest="pip_executable", help='Use this pip.exe', nargs='?', default=Configuration.pip_executable, const=None)
parser.add_argument("-epa", "--extra_pip_args", dest="extra_pip_args", help='Extra pip.exe args like: --no-index', nargs='?', default=Configuration.extra_pip_args, const=None)
# parser.add_argument("-pip2tgz", "--pip_2_tgz_executable", dest="pip_2_tgz_executable", help='Use this pip2tgz.exe', nargs='?', default=Configuration.pip_2_tgz_executable, const=None)
# parser.add_argument("-dir2pi", "--dir_2_pi_executable", dest="dir_2_pi_executable", help='Use this dir2pi.exe', nargs='?', default=Configuration.dir_2_pi_executable, const=None)
parser.add_argument("-l", "--log_file", help="File path to write logs to", nargs='?', default=None, const=Configuration.log_file,)
parser.add_argument("-v", "--verbose", help="More awesome printings.", action='store_true')

received_args = None


def read_args(args_list):
    log_info("Reading received args: {}".format(args_list))
    global received_args

    if len(args_list) == 0:
        parser.print_help()
        MyGlobals.terminate_program(0)

    try:
        received_args = parser.parse_args()
    except SystemExit as errorCode:
        MyGlobals.terminate_program(errorCode)
    except BaseException as errorMsg:
        log_error("Error - Failed to parse received args: {}\n{}".format(args_list, errorMsg))
        MyGlobals.terminate_program(1)

    Configuration.pip_executable = received_args.pip_executable
    Configuration.extra_pip_args = received_args.extra_pip_args
    Configuration.is_verbose = received_args.verbose
    Configuration.export_packages = received_args.export_packages
    if received_args.export_to:
        Configuration.export_to = received_args.export_to
        Configuration.exported_files_json_file = path.join(received_args.export_to, "simple", "exported_files.json")
    Configuration.import_packages = received_args.import_packages
    Configuration.import_from = received_args.import_from
    Configuration.log_file = received_args.log_file

    log_debug("Finished reading args successfully")



def log_info(msg=""):
    logging.getLogger(__name__).info(msg)


def log_debug(msg=""):
    logging.getLogger(__name__).debug(msg)


def log_error(msg=""):
    logging.getLogger(__name__).error(msg)

