# This module contains tasks execution functions to be used by other scripts

# System
import logging
from time import sleep

# Modules
from MyModules import TaskThread
from MyModules import MyGlobals

all_tasks = []
all_tasks_execution_result = True
threads = []
are_threads_running = False
should_abort_all = False
abort_more_info = ""


def execute_all_tasks():
    global all_tasks_execution_result
    global should_abort_all
    global abort_more_info
    log_info("Executing all tasks")

    for task in all_tasks:
        if should_abort_all:
            task.set_task_result(False, abort_more_info)
            continue
        log_debug("Processing task: {}".format(task.name))
        if task.wait_for_other_threads_to_finish_before_starting:
            wait_for_running_threads_to_finish()

        if task.wait_before_executing_sec:
            wait_before_executing(task.wait_before_executing_sec, task.name)

        if task.own_thread:
            start_task_in_new_thread(task)
        else:
            execute_single_task(task)

    wait_for_running_threads_to_finish()
    log_debug("Finished executing all tasks")
    return all_tasks_execution_result


def start_task_in_new_thread(task):
    global are_threads_running
    are_threads_running = True
    log_debug("Starting new thread on task: {}".format(task.name))
    t = TaskThread.TaskThread(task, task.name)
    t.start()
    threads.append(t)


def wait_for_running_threads_to_finish():
    global are_threads_running
    global should_abort_all
    global abort_more_info
    if not are_threads_running:
        return
    log_debug("Waiting for threads to finsih")
    global all_tasks_execution_result
    for t in threads:
        t.join()
        if t.task.abort_tasks_execution_on_failure and not t.task.result:
            log_info("Task: {} failure. Stopping execution of next tasks due to AbortTasksExecutionOnFailure=True flag.".format(t.task.name))
            abort_more_info = "Aborted due to failure of task: {}".format(t.task.name)
            should_abort_all = True
        if t.task.ignore_task_result:
            continue
        all_tasks_execution_result = all_tasks_execution_result and t.task.result
    log_debug("Finished waiting for threads to finsih")
    are_threads_running = False


def execute_single_task(task):
    global all_tasks_execution_result
    global should_abort_all
    global abort_more_info
    log_debug("Executing task: {}".format(task.name))
    task.execute()
    log_debug("Finished executing task: {}".format(task.name))

    if task.abort_tasks_execution_on_failure and not task.result:
        log_info("Task: {} failure. Stopping execution of next tasks due to AbortTasksExecutionOnFailure=True flag.".format(task.name))
        abort_more_info = "Aborted due to failure of task: {}".format(task.name)
        should_abort_all = True
    if task.ignore_task_result:
        return
    all_tasks_execution_result = all_tasks_execution_result and task.result


def wait_before_executing(sec, task_name):
    log_debug("Waiting {} seconds before executing {}".format(sec, task_name))
    MyGlobals.sleep(sec)
    return


def print_summary():
    summary_str = "Summary:\n============== Tasks Summary ==============\n"
    summary_str += "Threads: {}\n".format(len(threads))
    for t in all_tasks:
        summary_str += "Task: '{}' - ".format(t.name)
        summary_str += "SUCCESS [{}]\n".format(t.time_took) if t.result else "FAILURE [{}] <<-- {}\n".format(t.time_took, t.more_info)
    summary_str += "Execution Result: {}".format("Successful" if get_all_tasks_execution_result() else "Failed")
    log_info(summary_str)


def print_tasks_info():
    tasks_info_str = "Info:\n============== Tasks Info ==============\n"
    for t in all_tasks:
        tasks_info_str += "Task: '{}' - ".format(t.name)
        tasks_info_str += "vm_name: {}, vm_addr: {}, vm_port: {}, ssh_user: {}, ssh_pass: {}\n".format(t.vm_name, t.vm_addr, t.vm_port, t.ssh_user, t.ssh_pass)
    log_info(tasks_info_str)


def get_all_tasks_execution_result():
    return all_tasks_execution_result


def log_info(msg=""):
    logging.getLogger(__name__).info(msg)


def log_debug(msg=""):
    logging.getLogger(__name__).debug(msg)


def log_error(msg=""):
    logging.getLogger(__name__).error(msg)

