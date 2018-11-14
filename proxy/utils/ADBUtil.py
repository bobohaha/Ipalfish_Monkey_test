import os
from proxy.utils.LogUtil import LogUtil
from proxy.utils.PathUtil import PathUtil
import subprocess
import time


class ADBUtil:
    def __init__(self):
        pass

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
            proc.kill()
            proc.communicate()
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
        LogUtil.log("press_down: pid :" + str(proc.pid))
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
        std_result, std_error = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                                                 stderr=subprocess.PIPE).communicate()
        if std_result is not None:
            return std_result.strip()
        else:
            return std_error.strip()

    @staticmethod
    def get_installed_package_version(serial, package_name):
        command = "adb -s " + serial + " shell dumpsys package " + package_name \
                  + " | grep versionCode " \
                    "| awk -F' '  '{print $1}' " \
                    "| awk -F'=' '{print $2}' " \
                    "| awk '{if($1>1) {print $1}}'"
        print command
        std_result, std_error = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                                                 stderr=subprocess.PIPE).communicate()
        if std_result is not None:
            return std_result.strip()
        else:
            return std_error.strip()

    @staticmethod
    def broadcast_action(serial, action_name):
        LogUtil.log_start("broadcast_action: " + action_name)
        command = "adb -s " + serial + " shell am broadcast -a " + action_name
        os.system(command)
        LogUtil.log_end("broadcast_action: " + action_name)

    @staticmethod
    def wait_for_device(serial):
        LogUtil.log_start("wait_for_device")
        command = "adb -s " + serial + "wait-for-device"
        os.system(command)
        LogUtil.log_end("wait_for_device")

    @staticmethod
    def wait_for_reboot_complete(serial):
        while True:
            status = ADBUtil.get_prop(serial, "sys.boot_completed")
            if "1" in status and len(status.strip("\n").strip()) == 1:
                print "boot completed"
                break
            else:
                print "boot not completed wait,after five seconds check"
                time.sleep(5)
