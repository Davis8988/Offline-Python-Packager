# This module uses dir2pi module of pip2pi project. Check it ou by executing: pip install pip2pi

# System
import logging
from libpip2pi import commands

# Modules
from MyModules import MyGlobals


def index_packages_dir(dir_path):
    log_info("Indexing offline packages dir: {}".format(dir_path))
    try:
        exit_code = commands.dir2pi(["dir2pi", dir_path, "--no-symlink"])
        if exit_code != 0:
            log_error("Error while indexing dir: {}\nExit with: {}".format(dir_path, exit_code))
            MyGlobals.terminate_program(1)
    except BaseException as error_msg:
        log_error("Error while indexing dir: {}\n{}".format(dir_path, error_msg))
        MyGlobals.terminate_program(1)

def log_info(msg=""):
    logging.getLogger(__name__).info(msg)


def log_debug(msg=""):
    logging.getLogger(__name__).debug(msg)


def log_error(msg=""):
    logging.getLogger(__name__).error(msg)

