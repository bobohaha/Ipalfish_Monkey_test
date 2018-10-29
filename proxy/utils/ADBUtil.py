import os
from proxy.utils.LogUtil import LogUtil
from proxy.utils.PathUtil import PathUtil

from time import sleep
import subprocess

class ADBUtil:

    CURRENT_PATH = PathUtil.get_file_path(__file__)

    @staticmethod
    def reboot_to_bootloader(serial):
        LogUtil.log_start("reboot_to_bootloader")

        command = "adb -s " + serial + " reboot bootloader"
        LogUtil.log(command)
        os.system(command)

        LogUtil.log_end("reboot_to_bootloader")

    @staticmethod
    def reboot(serial):
        LogUtil.log_start("reboot")

        command = "adb -s " + serial + " reboot"
        LogUtil.log(command)
        os.system(command)

        LogUtil.log_end("reboot")

    @staticmethod
    def install(serial, apk_path):
        LogUtil.log_start("install")

        command = "adb -s " + serial + " install -r -d " + apk_path
        LogUtil.log(command)
        os.system(command)

        LogUtil.log_end("install")

    @staticmethod
    def install_and_async_monitor_google_dialog_to_workaround(serial, apk_path):
        LogUtil.log_start("install_and_async_monitor_google_dialog_to_workaround")

        command = "adb -s " + serial + " install -r -d " + apk_path + " & "

        proc = ADBUtil.press_down(serial)

        output = os.popen(command)
        text = output.read().strip()

        try:
            proc.terminate()
        except:
            pass

        if text.endswith("Success"):
            print "%s install success" % apk_path
        else:
            print "%s install failure" % apk_path

        LogUtil.log_end("install_and_async_monitor_google_dialog_to_workaround")

    @staticmethod
    def press_down(serial):
        proc = subprocess.Popen(["sh", ADBUtil.CURRENT_PATH + '/press_down.sh', serial])
        print proc.pid
        return proc

    @staticmethod
    def move(serial, device_path, local_path):
        command = "adb -s " + serial + " shell mv " + device_path + " " + local_path
        print command
        os.system(command)

    @staticmethod
    def pull(serial, device_path, local_path):
        command = "adb -s " + serial + " pull " + device_path + " " + local_path
        print command
        os.system(command)

    @staticmethod
    def rm(serial, device_path):
        command = "adb -s " + serial + " shell rm -rf " + device_path
        print command
        os.system(command)

    @staticmethod
    def mkdir_p(serial, device_path):
        command = "adb -s " + serial + " shell mkdir -p " + device_path
        print command
        os.system(command)

    @staticmethod
    def get_prop(serial, prop):
        command = "adb -s " + serial + " shell getprop " + prop
        print command
        std_result, std_error = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        if std_result != None:
            return std_result.strip()
        else:
            return std_error.strip()

#ADBUtil.install_and_press_down("117cf09", "./app-miui-xxxhdpi-debug.apk ")