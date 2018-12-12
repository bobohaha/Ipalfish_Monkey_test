import os
import subprocess

from PathUtil import PathUtil


class ShellUtil:
    def __init__(self):
        pass

    @staticmethod
    def execute_shell(command, output=False):
        print command
        if not output:
            os.system(command)
            return
        else:
            std_result, std_error = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                                                     stderr=subprocess.PIPE).communicate()
            print "std_result: " + str(std_result), "std_error: " + str(std_error)
            return std_result, std_error

    @staticmethod
    def rename_sub_string(origin_str, target_str, file_path, file_name_regex):
        path = PathUtil(__file__)
        path.chdir(file_path)
        command = "rename 's/" + origin_str + "/" + target_str + "/g' " + file_name_regex
        ShellUtil.execute_shell(command)
        path.back()
