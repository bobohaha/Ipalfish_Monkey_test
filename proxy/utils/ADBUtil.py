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
    def root_and_remount(serial):
        command = "adb -s " + serial + " root"
        os.system(command)
        command = "adb -s " + serial + " remount"
        os.system(command)

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
        command = "settings put global verifier_verify_adb_installs 0"
        ADBUtil.execute_shell(serial, command)
        LogUtil.log_end("set_adb_install_enable")

    @staticmethod
    def check_adb_install_enable(serial):
        LogUtil.log_start("check_adb_install_enable")
        command = "settings get global verifier_verify_adb_installs"
        std_result, std_error = ADBUtil.execute_shell(serial, command, True)
        if "0" in std_result:
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
        command = "mv " + device_path + " " + local_path
        ADBUtil.execute_shell(serial, command)

    @staticmethod
    def pull(serial, device_path, local_path):
        command = "adb -s " + serial + " pull " + device_path + " " + local_path
        print command
        os.system(command)

    @staticmethod
    def push(serial, local_path, device_path="/sdcard", quiet=True):
        ADBUtil.mkdir_p(serial, device_path)
        command = "adb -s " + serial + " push " + local_path + " " + device_path
        if quiet:
            command += " 2>&1 >/dev/null"
        print command
        os.system(command)

    @staticmethod
    def rm(serial, device_path):
        command = "rm -rf " + device_path
        ADBUtil.execute_shell(serial, command)

    @staticmethod
    def clear_pkg_cache(serial, pkg):
        command = "pm clear " + pkg
        ADBUtil.execute_shell(serial, command)

    @staticmethod
    def mkdir_p(serial, device_path):
        command = "mkdir -p " + device_path
        ADBUtil.execute_shell(serial, command)

    @staticmethod
    def get_prop(serial, prop):
        command = "getprop " + prop
        std_result, std_error = ADBUtil.execute_shell(serial, command, True)
        if std_result is not None:
            return std_result.strip()
        else:
            return std_error.strip()

    @staticmethod
    def set_prop(serial, prop, value):
        command = "setprop " + prop + " " + value
        ADBUtil.execute_shell(serial, command)

    @staticmethod
    def get_installed_package_version(serial, package_name):
        command = "dumpsys package " + package_name \
                  + " | grep versionCode " \
                    "| awk -F' '  '{print $1}' " \
                    "| awk -F'=' '{print $2}' " \
                    "| awk '{if($1>1) {print $1}}'"
        std_result, std_error = ADBUtil.execute_shell(serial, command, True)
        if std_result is not None:
            return std_result.strip()
        else:
            return std_error.strip()

    @staticmethod
    def broadcast_action(serial, action_name):
        LogUtil.log_start("broadcast_action: " + action_name)
        command = "am broadcast -a " + action_name
        ADBUtil.execute_shell(serial, command)
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
            command = "dumpsys window | grep mFocusedApp | grep -v AppWindowToken | grep " + package
            std_result, std_error = ADBUtil.execute_shell(serial, command, True)
            if std_result is not None and len(std_result) != 0:
                return True
            else:
                return False

        in_miui_oobe = ADBUtil.is_in_oobe(serial, package="com.android.provision")
        in_google_oobe = ADBUtil.is_in_oobe(serial, package="com.google.android.setupwizard")
        return in_miui_oobe or in_google_oobe

    @staticmethod
    def wait_for_enter_system(serial):
        command = "dumpsys window | grep mFocusedApp"
        while True:
            std_result, std_error = ADBUtil.execute_shell(serial, command, True)
            if std_result is not None and len(std_result) != 0 \
                    and "mFocusedApp=null" not in std_result:
                return True
            else:
                time.sleep(5)

    @staticmethod
    def power_on(serial):
        command = "input keyevent 224"
        ADBUtil.execute_shell(serial, command)

    @staticmethod
    def take_screenshot(serial, out_put_file_path):
        ADBUtil.power_on(serial)
        ADBUtil.root_and_remount(serial)
        command = "screencap -p " + out_put_file_path
        ADBUtil.execute_shell(serial, command, True)

    @staticmethod
    def execute_shell(serial, shell_command, output=False):
        command = "adb -s " + serial + " shell " + shell_command
        print(command)
        if output is False:
            os.system(command)
            return
        else:
            std_result, std_error = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                                                     stderr=subprocess.PIPE).communicate()
            print "std_result: " + str(std_result), "std_error: " + str(std_error)
            return std_result, std_error

    @staticmethod
    def silence_and_disable_notification_in_device(serial):
        ADBUtil.root_and_remount(serial)
        ADBUtil.execute_shell(serial, "settings put global policy_control immersive.full=*")
        ADBUtil.execute_shell(serial, "pm disable com.android.systemui")
        ADBUtil.execute_shell(serial, "input keyevent 164")
        pass
