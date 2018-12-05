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
        os.system(command)

        LogUtil.log_end("reboot_to_bootloader")

    @staticmethod
    def reboot(serial):
        LogUtil.log_start("reboot")

        command = "adb -s " + serial + " reboot"
        os.system(command)

        LogUtil.log_end("reboot")

    @staticmethod
    def install(serial, apk_path):
        LogUtil.log_start("install")

        if not ADBUtil.check_adb_install_enable(serial):
            ADBUtil.set_adb_install_enable(serial)

        command = "adb -s " + serial + " install -r -d " + apk_path
        std_result, std_error = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                                                 stderr=subprocess.PIPE).communicate()
        print "std_result: " + std_result, "std_error: " + std_error

        if "success" in std_result.lower() or "success" in std_error.lower():
            print "%s install success" % apk_path
            _rst = True
        else:
            print "%s install failure" % apk_path
            _rst = False

        LogUtil.log_end("install")
        return _rst

    @staticmethod
    def try_install(serial, apk_path):
        try_time = 3
        while try_time > 0:
            install_rst = ADBUtil.install(serial, apk_path)
            if install_rst:
                return True
            else:
                try_time -= 1
        return False

    @staticmethod
    def set_adb_install_enable(serial):
        LogUtil.log_start("set_adb_install_enable")

        command = "adb -s " + serial + " shell settings put global verifier_verify_adb_installs 0"
        LogUtil.log(command)
        os.system(command)

        LogUtil.log_end("set_adb_install_enable")

    @staticmethod
    def check_adb_install_enable(serial):
        LogUtil.log_start("check_adb_install_enable")

        command = "adb -s " + serial + " shell settings get global verifier_verify_adb_installs"

        output = os.popen(command)
        text = output.read().strip()

        LogUtil.log("check_adb_install_enable: " + text)

        if text.endswith("0"):
            LogUtil.log_end("check_adb_install_enable: True")
            return True
        else:
            LogUtil.log_end("check_adb_install_enable: False")
            return False

    @staticmethod
    def press_down(serial):
        press_down_command = ADBUtil.CURRENT_PATH + '/press_down.sh'
        proc = subprocess.Popen(["sh", press_down_command, serial])
        LogUtil.log("press_down: pid :" + str(proc.pid))
        return proc, press_down_command

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

    @staticmethod
    def wait_and_check_is_in_oobe(serial):
        wait_time = 1 * 60
        while wait_time > 0:
            result = ADBUtil.is_in_oobe(serial)
            if result:
                return result
            else:
                wait_time_gap = 5
                time.sleep(wait_time_gap)
                wait_time -= wait_time_gap
        return False

    @staticmethod
    def is_in_oobe(serial, package=None):
        if package is not None:
            command = "adb -s " + serial \
                      + " shell dumpsys window | grep mFocusedApp | grep -v AppWindowToken | grep " + package
            std_result, std_error = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                                                     stderr=subprocess.PIPE).communicate()
            if std_result is not None and len(std_result) != 0:
                print std_result
                return True
            else:
                print std_result, std_error
                return False

        in_miui_oobe = ADBUtil.is_in_oobe(serial, package="com.android.provision")
        in_google_oobe = ADBUtil.is_in_oobe(serial, package="com.google.android.setupwizard")
        return in_miui_oobe or in_google_oobe

    @staticmethod
    def wait_for_enter_system(serial):
        command = "adb -s " + serial \
                  + " shell dumpsys window | grep mFocusedApp"

        while True:
            std_result, std_error = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                                                     stderr=subprocess.PIPE).communicate()
            if std_result is not None and len(std_result) != 0 \
                    and "mFocusedApp=null" not in std_result:
                print "std_result: " + std_result
                return True
            else:
                print "std_result: " + str(std_result), "std_error: " + str(std_error)
                time.sleep(5)
