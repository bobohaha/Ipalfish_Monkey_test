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

    @staticmethod
    def get_apk_version_code(file_path):
        command = "aapt d badging " + file_path
        std_out, std_err = ShellUtil.execute_shell(command, True)
        try:
            for line in std_out.split("\n"):
                if "versionCode" in line:
                    version_code = line.split("versionCode=")[1].split("'")[1]
                    return int(version_code)
        except Exception, why:
            print "get_apk_version_code error: ", why
        print "get_apk_version_code failed"
        return 0

    @staticmethod
    def get_apk_package_name(file_path):
        command = "aapt d badging " + file_path
        std_out, std_err = ShellUtil.execute_shell(command, True)
        try:
            for line in std_out.split("\n"):
                if "package: name=" in line:
                    package_name = line.split("package: name=")[1].split("'")[1]
                    return package_name
        except Exception, why:
            print "get_apk_package_name error: ", why

        print "get_apk_package_name failed"
        return ""
