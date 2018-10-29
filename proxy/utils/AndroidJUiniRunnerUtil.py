import os


class AndroidJUiniRunnerUtil:

    @staticmethod
    def get_adb_command(serial, class_name, pkg_name):
        command = "adb -s " + serial + " shell am instrument -w -r -e debug false -e class " \
                  + class_name + " " + pkg_name \
                  + "/android.support.test.runner.AndroidJUnitRunner"

        print command
        return command

    @staticmethod
    def run_adb_command(serial, class_name, pkg_name):
        command = AndroidJUiniRunnerUtil.get_adb_command(serial, class_name, pkg_name)
        os.system(command)

    @staticmethod
    def run_adb_command_output(serial, class_name, pkg_name, file_name):
        command = AndroidJUiniRunnerUtil.get_adb_command(serial, class_name, pkg_name)
        command = command + " | tee " + file_name
        os.system(command)











