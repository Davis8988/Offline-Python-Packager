# This module contains functions to execute tasks as threads
# Sources:
#  https://docs.python.org/3/library/os.html


import threading
import logging


class TaskThread(threading.Thread):
    def __init__(self, task, name):
        threading.Thread.__init__(self)
        self.task = task
        self.name = name

    def run(self):
        log_info("Thread {} executing".format(self.name))
        execute_task(self)
        log_debug("Thread {} finished executing".format(self.name))


def execute_task(self):
    self.task.execute()


def log_info(msg=""):
    logging.getLogger(__name__).info(msg)

def log_debug(msg=""):
    logging.getLogger(__name__).debug(msg)

def log_error(msg=""):
    logging.getLogger(__name__).error(msg)

