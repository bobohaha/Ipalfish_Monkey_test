import os

from proxy.utils.PathUtil import PathUtil


class AndroidJUnitRunnerUtil:
    def __init__(self):
        pass

    @staticmethod
    def get_adb_command(serial, class_name, pkg_name):
        command = "adb -s " + serial + " shell am instrument -w -r -e debug false -e class " \
                  + class_name + " " + pkg_name \
                  + "/android.support.test.runner.AndroidJUnitRunner"

        print command
        return command

    @staticmethod
    def run_adb_command(serial, class_name, pkg_name):
        command = AndroidJUnitRunnerUtil.get_adb_command(serial, class_name, pkg_name)
        os.system(command)

    @staticmethod
    def run_adb_command_output(serial, class_name, pkg_name, file_name):
        command = AndroidJUnitRunnerUtil.get_adb_command(serial, class_name, pkg_name)
        command = command + " | tee " + file_name
        os.system(command)

    @staticmethod
    def get_adb_command_with_extra_param(serial, class_name, pkg_name, extra_param_dict):
        if not extra_param_dict:
            return AndroidJUnitRunnerUtil.get_adb_command(serial, class_name, pkg_name)

        command = "adb -s " + serial + " shell am instrument -w -r"
        for extra_param_key in extra_param_dict.keys():
            command = command + " -e " + extra_param_key + " " + extra_param_dict[extra_param_key]
        command = command + " -e class " + class_name + " " + pkg_name + "/android.support.test.runner.AndroidJUnitRunner"

        print command
        return command

    @staticmethod
    def run_adb_command_with_extra_param(serial, class_name, pkg_name, extra_param_dict):
        command = AndroidJUnitRunnerUtil.get_adb_command_with_extra_param(serial,
                                                                          class_name,
                                                                          pkg_name,
                                                                          extra_param_dict)
        os.system(command)

    @staticmethod
    def run_adb_command_output_with_extra_param(serial, class_name, pkg_name, file_name,
                                                extra_param_dict):
        command = AndroidJUnitRunnerUtil.get_adb_command_with_extra_param(serial,
                                                                          class_name,
                                                                          pkg_name,
                                                                          extra_param_dict)
        command = command + " | tee " + file_name
        os.system(command)

    @staticmethod
    def analysis_instrument_run_result(file_name):
        rst = None

        if os.path.exists("%s" % file_name) is False:
            print("file isn't exist.")
            return rst

        for line in open("%s" % file_name, 'r'):
            if "Failure" in line:
                print("Instrument run failure")
                rst = False
                break

            if "OK " in line:
                print("Instrument run OK")
                rst = True
                break

        if rst is None:
            print("Instrument run  unfinished")

        return rst
