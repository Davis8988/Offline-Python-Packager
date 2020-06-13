# This module contains classes to be used by other scripts

# System
import logging
import time
from datetime import timedelta

# Modules
from MyModules import MyGlobals
from MyModules import Configuration
from MyModules import VirtualBox


section_task_task_name_name = "TaskName"
section_task_own_thread_name = "OwnThread"
section_task_wait_for_other_threads_to_finish_before_starting_name = "WaitForOtherThreadsToFinishBeforeStarting"


class Task:
    def __init__(self, name, vm_name, vm_addr, vm_port, ssh_user, ssh_pass, result=None, more_info="Not Started Yet", own_thread=False, wait_for_other_threads_to_finish_before_starting=False,
                 ssh_client=None, connect_to_vm_retry_count=None, wait_before_retry_sec=None, connect_timeout_sec=None, abort_tasks_execution_on_failure=False, wait_before_executing_sec=None, ignore_task_result=False,
                 start_vm_when_done=False, power_off_vm_when_done=False):
        self.start_time = None
        self.end_time = None
        self.time_took = None
        self.name = name
        self.result = result
        self.more_info = more_info
        self.own_thread = own_thread
        self.wait_for_other_threads_to_finish_before_starting = wait_for_other_threads_to_finish_before_starting
        self.vm_name = vm_name
        self.vm_addr = vm_addr
        self.vm_port = vm_port
        self.ssh_user = ssh_user
        self.ssh_pass = ssh_pass
        self.ssh_client = ssh_client
        self.connect_to_vm_retry_count = connect_to_vm_retry_count
        self.wait_before_retry_sec = wait_before_retry_sec
        self.connect_timeout_sec = connect_timeout_sec
        self.abort_tasks_execution_on_failure = abort_tasks_execution_on_failure
        self.wait_before_executing_sec = wait_before_executing_sec
        self.ignore_task_result = ignore_task_result
        self.start_vm_when_done = start_vm_when_done
        self.power_off_vm_when_done = power_off_vm_when_done

    def set_task_result(self, result=False, more_info=""):
        self.result = result
        self.more_info = more_info

    def pre_execute_actions(self, start_msg):
        self.start_time = time.time()
        log_debug(start_msg)

    def execute(self):
        pass

    def post_execute_actions(self, action_dict):
        if not action_dict["Result"]:
            self.set_task_result(result=action_dict["Result"], more_info=action_dict["MoreInfo"])
            return action_dict
        action_dict = self.common_options_actions()
        self.end_time = time.time()
        self.time_took = str(timedelta(seconds=self.end_time - self.start_time)).split(".")[0]
        more_info = self.SUCCESS_TASK_MSG if action_dict["Result"] else action_dict["MoreInfo"]
        self.set_task_result(result=action_dict["Result"], more_info=more_info)

    def common_options_actions(self):
        action_dict = {"Result": True, "MoreInfo": ""}
        if self.start_vm_when_done:
            action_dict = VirtualBox.start_vm(self.vm_name)
        if self.power_off_vm_when_done:
            action_dict = VirtualBox.power_off_vm(self.vm_name)
        return action_dict



def read_task_common_attributes_dict(cur_section_values):
    try:
        task_name = cur_section_values.name if None is cur_section_values.get(section_task_task_name_name) else MyGlobals.remove_surrounding_quotes(MyGlobals.expand_variable(cur_section_values[section_task_task_name_name]))
        own_thread = False if None is cur_section_values.get(section_task_own_thread_name) else MyGlobals.convert_and_expand_str_to_boolean(cur_section_values[section_task_own_thread_name])
        wait_for_other_threads_to_finish_before_starting = False if None is cur_section_values.get(section_task_wait_for_other_threads_to_finish_before_starting_name) else MyGlobals.convert_and_expand_str_to_boolean(cur_section_values[section_task_wait_for_other_threads_to_finish_before_starting_name])
        vm_name = Configuration.vm_name if None is cur_section_values.get("VMName") else MyGlobals.remove_surrounding_quotes(MyGlobals.expand_variable(cur_section_values["VMName"]))
        vm_addr = Configuration.vm_addr if None is cur_section_values.get("VMAddr") else MyGlobals.remove_surrounding_quotes(MyGlobals.expand_variable(cur_section_values["VMAddr"]))
        vm_port = Configuration.vm_port if None is cur_section_values.get("VMPort") else MyGlobals.remove_surrounding_quotes(MyGlobals.expand_variable(cur_section_values["VMPort"]))
        ssh_user = Configuration.ssh_user if None is cur_section_values.get("SSHUser") else MyGlobals.remove_surrounding_quotes(MyGlobals.expand_variable(cur_section_values["SSHUser"]))
        ssh_pass = Configuration.ssh_pass if None is cur_section_values.get("SSHPass") else MyGlobals.remove_surrounding_quotes(MyGlobals.expand_variable(cur_section_values["SSHPass"]))
        connect_to_vm_retry_count = Configuration.connect_to_vm_retry_count_default if None is cur_section_values.get("ConnectToVMRetriesCount") else MyGlobals.convert_and_expand_str_to_integer(cur_section_values["ConnectToVMRetriesCount"])
        wait_before_retry_sec = Configuration.wait_before_retry_sec_default if None is cur_section_values.get("WaitBeforeRetrySec") else MyGlobals.convert_and_expand_str_to_integer(cur_section_values["WaitBeforeRetrySec"])
        connect_timeout_sec = Configuration.connect_timeout_sec_default if None is cur_section_values.get("ConnectTimeoutSec") else MyGlobals.convert_and_expand_str_to_integer(cur_section_values["ConnectTimeoutSec"])
        abort_tasks_execution_on_failure = Configuration.abort_tasks_execution_on_failure_default if None is cur_section_values.get("AbortTasksExecutionOnFailure") else MyGlobals.convert_and_expand_str_to_boolean(cur_section_values["AbortTasksExecutionOnFailure"])
        wait_before_executing_sec = Configuration.wait_before_executing_sec_default if None is cur_section_values.get("WaitBeforeExecutingSec") else MyGlobals.convert_and_expand_str_to_integer(cur_section_values["WaitBeforeExecutingSec"])
        ignore_task_result = Configuration.wait_before_executing_sec_default if None is cur_section_values.get("IgnoreTaskResult") else MyGlobals.convert_and_expand_str_to_boolean(cur_section_values["IgnoreTaskResult"])
        start_vm_when_done = Configuration.start_vm_when_done_default if None is cur_section_values.get("StartVMWhenDone") else MyGlobals.convert_and_expand_str_to_boolean(cur_section_values["StartVMWhenDone"])
        power_off_vm_when_done = Configuration.power_off_vm_when_done_default if None is cur_section_values.get("PowerOffVMWhenDone") else MyGlobals.convert_and_expand_str_to_boolean(cur_section_values["PowerOffVMWhenDone"])

        return {
            "task_name" : task_name,
            "own_thread" : own_thread,
            "wait_for_other_threads_to_finish_before_starting" : wait_for_other_threads_to_finish_before_starting,
            "vm_name" : vm_name,
            "vm_addr" : vm_addr,
            "vm_port" : vm_port,
            "ssh_user" : ssh_user,
            "ssh_pass" : ssh_pass,
            "connect_to_vm_retry_count" : connect_to_vm_retry_count,
            "wait_before_retry_sec" : wait_before_retry_sec,
            "connect_timeout_sec" : connect_timeout_sec,
            "abort_tasks_execution_on_failure" : abort_tasks_execution_on_failure,
            "wait_before_executing_sec" : wait_before_executing_sec,
            "ignore_task_result" : ignore_task_result,
            "start_vm_when_done" : start_vm_when_done,
            "power_off_vm_when_done" : power_off_vm_when_done
        }
    except BaseException as errorMsg:
        log_error("Error - Failed reading import common task attributes in section: {}\n{}".format(cur_section_values.name, errorMsg))
    return None


def check_common_attributes_dict(common_attr_dict):
    action_dict = {"Result": True, "MoreInfo": ""}
    start_vm_when_done = common_attr_dict.get("StartVMWhenDone")
    power_off_vm_when_done = common_attr_dict.get("PowerOffVMWhenDone")
    if start_vm_when_done and power_off_vm_when_done:
        action_dict["Result"] = False
        action_dict["MoreInfo"] = "Cannot have contradicting entries in task section: 'StartVMWhenDone=True' & 'PowerOffVMWhenDone=True'. Turn one of them off."
        log_error(action_dict["MoreInfo"])
    return action_dict




def log_info(msg=""):
    logging.getLogger(__name__).info(msg)


def log_debug(msg=""):
    logging.getLogger(__name__).debug(msg)


def log_error(msg=""):
    logging.getLogger(__name__).error(msg)

