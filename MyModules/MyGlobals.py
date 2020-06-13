# This module contains global functions to be used by other scripts

import os
import subprocess
import sys
import shutil
import logging
import time
import distutils
from distutils import dir_util
from ast import literal_eval
from glob import glob

# Modules
from MyModules import Configuration

os_error_directory_not_empty_error_number = 41
os_windoes_error_directory_not_empty_error_number = 145


def copy_file(src_path, dest_path):
    # ┌──────────────────┬────────┬───────────┬───────┬────────────────┐
    # │     Function     │ Copies │   Copies  │Can use│   Destination  │
    # │                  │metadata│permissions│buffer │may be directory│
    # ├──────────────────┼────────┼───────────┼───────┼────────────────┤
    # │shutil.copy       │   No   │    Yes    │   No  │      Yes       │
    # │shutil.copyfile   │   No   │     No    │   No  │       No       │
    # │shutil.copy2      │  Yes   │    Yes    │   No  │      Yes       │
    # │shutil.copyfileobj│   No   │     No    │  Yes  │       No       │
    # └──────────────────┴────────┴───────────┴───────┴────────────────┘
    action_dict = {"Result" : True, "MoreInfo" : ""}
    try:
        shutil.copy2(src_path, dest_path)
    except BaseException as error_msg:
        log_error("Error - Failed to copy file '{}' to: '{}'\n{}".format(src_path, dest_path, error_msg))
        action_dict['Result'] = False
        action_dict['MoreInfo'] = error_msg
    return action_dict


def copy_dir(src_path, dest_path, exclude=None, include=None):
    action_dict = {"Result": True, "MoreInfo": ""}
    try:
        if is_file(dest_path):
            action_dict['Result'] = False
            action_dict['MoreInfo'] = "Dest path is a file. Cannot copy a directory into a file."
            return action_dict
        else:
            action_dict = create_dir(dest_path)
            if not action_dict["Result"]:
                return action_dict
        include_or_exclude = include if None is not include else exclude
        dir_util.copy_tree(src_path, dest_path)
    except shutil.Error as shutil_err:
        try:
            log_debug("Got error - retrying..")
            errors = shutil_err.args[0]
            for error in errors:
                src, dst, msg = error
                # Get the path to the file in Gold dir here from src
                # shutil.copy2(src, dst)
                if dir_exists(dst):
                    remove_result = remove_dir(dst)
                    if not remove_result['Result']:
                        return remove_result
                shutil.copytree(src, dst, ignore=include_or_exclude)
        except BaseException as error_msg:
            log_error("Error - Failed to copy2 dir '{}' to: '{}'\n{}".format(src_path, dest_path, error_msg))
            action_dict['Result'] = False
            action_dict['MoreInfo'] = error_msg
    except BaseException as error_msg:
        log_error("Error - Failed to copy dir '{}' to: '{}'\n{}".format(src_path, dest_path, error_msg))
        action_dict['Result'] = False
        action_dict['MoreInfo'] = error_msg
    return action_dict


def copy_dir_2(src_path, dest_path, exclude=None, include=None):
    action_dict = {"Result": True, "MoreInfo": ""}
    if is_file(dest_path):
        action_dict['Result'] = False
        action_dict['MoreInfo'] = "Dest path is a file. Cannot copy a directory into a file."
        return action_dict
    include_or_exclude = include if None is not include else exclude
    errors = my_copytree(src_path, dest_path, ignore=include_or_exclude)
    if errors:
        action_dict['Result'] = False
        action_dict['MoreInfo'] = "See errors below:\n" + convert_copy_err_list_to_table(errors)
    return action_dict


def my_copytree(src, dst, symlinks=True, ignore=None):
    errors = []
    if not os.path.isdir(dst):
        action_dict = create_dir(dst)
        if not action_dict["Result"]:
            log_debug(action_dict['MoreInfo'])
            errors.append((src, dst, action_dict['MoreInfo']))
            return errors

    names = os.listdir(src)
    ignored_names = set() if None is ignore else ignore(src, names)

    for name in names:
        if name in ignored_names:
            continue
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if symlinks and os.path.islink(srcname):
                linkto = os.readlink(srcname)
                os.symlink(linkto, dstname)
            elif os.path.isdir(srcname):
                errs = my_copytree(srcname, dstname, symlinks, ignore)
                errors.extend(errs)
                return errors
            else:
                shutil.copy2(srcname, dstname)
        except (IOError, os.error) as error_msg:
            log_debug(str(error_msg))
            errors.append((srcname, dstname, str(error_msg)))
        except shutil.Error as error_msg:
            errors.extend(error_msg.args[0])
    try:
        shutil.copystat(src, dst)
    except WindowsError:
        pass
    except OSError as error_msg:
        log_debug(str(error_msg))
        errors.append((src, dst, str(error_msg)))

    return errors


def convert_copy_err_list_to_table(errors):
    converted_str = ''
    for src, dest, err in errors:
        converted_str += " -- Failed copy: {} to: {} - {}\n".format(src, dest, err)
    return converted_str


def expand_variable(variable):
    try:
        return os.path.expandvars(variable)
    except BaseException as error_msg:
        log_error("Error - Failed to expand variable: {}\n{}".format(variable, error_msg))
    return None


def file_exists(file_path):
    try:
        return os.path.isfile(file_path)
    except BaseException as error_msg:
        print("Error - Failed checking if file exists at: {}\n{}".format(file_path, error_msg))
    return False


def is_file(file_path):
    return file_exists(file_path)


def exists(some_path):
    try:
        return os.path.exists(some_path)
    except BaseException as error_msg:
        log_error("Error - Failed checking if path exists at: {}\n{}".format(some_path, error_msg))
    return False


def dir_exists(dir_path):
    try:
        return os.path.isdir(dir_path)
    except BaseException as error_msg:
        log_error("Error - Failed checking if dir exists at: {}\n{}".format(dir_path, error_msg))
    return False


def is_dir(dir_path):
    return dir_exists(dir_path)


def remove_surrounding_quotes(some_str):
    return str(some_str).strip().strip("\"")


def remove_dir(dir_path):
    action_dict = {"Result": True, "MoreInfo": ""}
    try:
        log_debug("Removing dir: {}".format(dir_path))
        shutil.rmtree(dir_path, onerror=rmtree_onerror_handlling)
    except BaseException as error_msg:
        log_error("Error - Failed removing dir at: {}\n{}".format(dir_path, error_msg))
        action_dict['Result'] = False
        action_dict['MoreInfo'] = error_msg
    return action_dict


def rmtree_onerror_handlling(func, path, exc_info):
    """
    Error handler for ``shutil.rmtree``.

    If the error is due to an access error (read only file)
    it attempts to add write permission and then retries.

    If the error is for another reason it re-raises the error.

    Usage : ``shutil.rmtree(path, onerror=onerror)``
    """
    import stat
    if not os.access(path, os.W_OK):
        # Is the error an access error ?
        os.chmod(path, stat.S_IWUSR)
        func(path)

    # OSError & Error numbers of directory-not-empty.
    #  Handle by: Sleep for a few moments and then try again (repeat few times if needed)
    elif exc_info[0] == OSError and (exc_info[1].errno == os_error_directory_not_empty_error_number or exc_info[1].errno == os_error_directory_not_empty_error_number):
        retries = Configuration.remove_dir_retry_count
        sleep_sec = Configuration.remove_dir_sleep_between_retries_sec
        os_error = True
        while retries > 0 and os_error:
            try:
                log_debug("Could not remove path: {}. Waiting for: {} seconds and retrying..".format(path, sleep_sec))
                sleep(sleep_sec)
                shutil.rmtree(path)
                os_error = False  # If shutil.rmtree() succeeded then no need to stay in the loop
                retries = retries - 1
            except OSError as error_msg:
                if error_msg.errno == os_error_directory_not_empty_error_number or error_msg.errno == os_error_directory_not_empty_error_number:
                    pass
                else:
                    raise
            except BaseException:
                raise
    else:
        raise


def remove_file(file_path):
    action_dict = {"Result": True, "MoreInfo": ""}
    try:
        log_debug("Removing file: {}".format(file_path))
        os.remove(file_path)
    except BaseException as error_msg:
        log_error("Error - Failed removing file at: {}\n{}".format(file_path, error_msg))
        action_dict['Result'] = False
        action_dict['MoreInfo'] = error_msg
    return action_dict


def create_dir(dir_path):
    action_dict = {"Result": True, "MoreInfo": ""}
    try:
        os.makedirs(dir_path)
        action_dict["MoreInfo"] = dir_path
    except FileExistsError:
        print("Dir exists..")
        pass
    except BaseException as error_msg:
        log_error("Error - Failed creating dir at: {}\n{}".format(dir_path, error_msg))
        action_dict['Result'] = False
        action_dict['MoreInfo'] = error_msg
    return action_dict


def convert_and_expand_str_to_list(some_string):
    some_string_expanded = remove_surrounding_quotes(expand_variable(some_string)).strip()
    return [x.strip() for x in some_string_expanded.split(",")]


def convert_and_expand_str_to_boolean(some_string):
    some_string_expanded = remove_surrounding_quotes(expand_variable(some_string)).strip()
    return str(some_string_expanded).lower() == "true"


def convert_and_expand_str_to_integer(some_string):
    some_string_expanded = remove_surrounding_quotes(expand_variable(some_string)).strip()
    return int(some_string_expanded)


def convert_and_expand_str_to_dictionary(some_string):
    some_string_expanded = remove_surrounding_quotes(expand_variable(some_string)).strip()
    return literal_eval(some_string_expanded)


def get_files_list_from_path(path_str):
    action_dict = {"Result": True, "MoreInfo": ""}
    try:
        files_list = glob(path_str)
        action_dict["MoreInfo"] = files_list
    except BaseException as error_msg:
        log_error(error_msg)
        action_dict["Result"] = False
        action_dict["MoreInfo"] = str(error_msg)
    return action_dict


def read_file_lines_as_list(file_path):
    action_dict = {"Result": True, "MoreInfo": ""}
    with open(file_path, 'r') as file:
        try:
            file_content = file.read().splitlines()
            action_dict["MoreInfo"] = file_content
        except (OSError, IOError) as error_msg:
            log_error(error_msg)
            action_dict["Result"] = False
            action_dict["MoreInfo"] = str(error_msg)
        except BaseException as error_msg:
            log_error("Fatal - ", error_msg, "\nTerminating..")
            terminate_program(1)
    return action_dict


def sleep(sec):
    try:
        time.sleep(sec)
    except BaseException as error_msg:
        log_error(error_msg)
    return


def include_patterns(*patterns):
    """Factory function that can be used with copytree() ignore parameter.

    Arguments define a sequence of glob-style patterns
    that are used to specify what files to NOT ignore.
    Creates and returns a function that determines this for each directory
    in the file hierarchy rooted at the source directory when used with
    shutil.copytree().
    """
    def _ignore_patterns(path, names):
        keep = set(name for pattern in patterns
                            for name in filter(names, pattern))
        ignore = set(name for name in names
                        if name not in keep and not os.path.isdir(os.path.join(path, name)))
        return ignore
    return _ignore_patterns


def terminate_program(exit_code, msg=""):
    if msg:
        print(msg)
    sys.exit(exit_code)


def get_files_list_flat(files_path):
    """Fetches a flat file list of a directory"""
    action_dict = {"Result": True, "MoreInfo": ""}
    try:
        if is_file(files_path):
            action_dict["MoreInfo"] = [files_path]
        else:
            action_dict["MoreInfo"] = [os.path.join(files_path,x) for x in os.listdir(files_path)]
    except BaseException as error_msg:
        action_dict["Result"] = False
        action_dict["MoreInfo"] = str(error_msg)
    return action_dict


def execute_command(cmnd):
    action_dict = {"Result": True, "MoreInfo": ""}
    log_debug("Executing: {}".format(cmnd))
    try:
        action_dict["MoreInfo"] = subprocess.check_output(cmnd, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as error_msg:
        action_dict["Result"] = False
        action_dict["MoreInfo"] = error_msg
    except BaseException as error_msg:
        log_error("Fatal - ", error_msg, "\nTerminating..")
        terminate_program(1)
    return action_dict


def log_info(msg=""):
    logging.getLogger(__name__).info(msg)


def log_debug(msg=""):
    logging.getLogger(__name__).debug(msg)


def log_error(msg=""):
    logging.getLogger(__name__).error(msg)

