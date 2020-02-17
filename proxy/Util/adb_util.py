import os
import platform
from .log_util import LogUtil
from .path_util import PathUtil
from .usb_util import UsbUtil
import subprocess
import time

from .shell_util import ShellUtil

adb = "adb.exe" if platform.system() == "Windows" else "adb"


class ADBUtil:
    def __init__(self):
        pass

    CURRENT_PATH = PathUtil.get_file_path(__file__)

    @staticmethod
    def root_and_remount(serial):
        ADBUtil.execute_adb_command(serial, "root")
        ADBUtil.execute_adb_command(serial, "remount")

    @staticmethod
    def reboot_to_bootloader(serial):
        LogUtil.log_start("reboot_to_bootloader")
        ADBUtil.execute_adb_command(serial, "reboot bootloader")
        LogUtil.log_end("reboot_to_bootloader")

    @staticmethod
    def reboot(serial):
        LogUtil.log_start("reboot")
        ADBUtil.do_reboot(serial)
        ADBUtil.wait_for_device(serial)
        ADBUtil.wait_for_reboot_complete(serial)
        ADBUtil.wait_for_enter_system(serial)
        LogUtil.log_end("reboot")

    @staticmethod
    def do_reboot(serial):
        LogUtil.log_start("do_reboot")
        ADBUtil.execute_adb_command(serial, "reboot")
        LogUtil.log_end("do_reboot")

    @staticmethod
    def install(serial, apk_path):
        LogUtil.log_start("install")
        if not ADBUtil.check_adb_install_enable(serial):
            ADBUtil.set_adb_install_enable(serial)
        _rst = ADBUtil.do_install(serial, apk_path)
        LogUtil.log_end("install")
        return _rst

    @staticmethod
    def do_install(serial, apk_path):
        LogUtil.log_start("do_install")
        std_out, std_err = ADBUtil.execute_adb_command(serial, "install -r -d -t {}".format(apk_path), True)
        if "success" in std_out.lower() or "success" in std_err.lower():
            print("%s install success" % apk_path)
            _rst = True
        else:
            print("%s install failure" % apk_path)
            _rst = False
        LogUtil.log_end("do_install")
        return _rst

    @staticmethod
    def try_install(serial, apk_path, try_time=3):
        while try_time > 0:
            install_rst = ADBUtil.install(serial, apk_path)
            if install_rst:
                return True
            else:
                try_time -= 1
                print('install apk failed, waiting for retry')
                time.sleep(30)
        return False

    @staticmethod
    def set_adb_install_enable(serial):
        LogUtil.log_start("set_adb_install_enable")
        command = "settings put global verifier_verify_adb_installs 0"
        ADBUtil.execute_shell(serial, command, output=True)
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
        press_down_command = os.path.join(ADBUtil.CURRENT_PATH, 'press_down.sh')
        proc = subprocess.Popen(["sh", press_down_command, serial])
        LogUtil.log("press_down: pid :" + str(proc.pid))
        return proc, press_down_command

    @staticmethod
    def move(serial, source_path, des_path):
        command = "mv {} {}".format(source_path, des_path)
        ADBUtil.execute_shell(serial, command)

    @staticmethod
    def pull(serial, device_path, local_path, quiet=False):
        tail = " 2>&1 >/dev/null" if quiet else ""
        command = "pull {} {}{}".format(device_path, local_path, tail)
        ADBUtil.execute_adb_command(serial, command)

    @staticmethod
    def push(serial, local_path, device_path="/sdcard", quiet=True):
        ADBUtil.mkdir_p(serial, device_path)
        tail = " 2>&1 >/dev/null" if quiet else ""
        command = "push {} {}{}".format(local_path, device_path, tail)
        ADBUtil.execute_adb_command(serial, command)

    @staticmethod
    def rm(serial, device_path):
        command = "rm -rf " + device_path
        ADBUtil.execute_shell(serial, command)

    @staticmethod
    def clear_pkg_cache(serial, pkg):
        command = "pm clear " + pkg
        ADBUtil.execute_shell(serial, command, output=True)

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
        ADBUtil.execute_shell(serial, command, output=True)

    @staticmethod
    def get_information_of_installed_package(serial, package_name, key_word=None):
        command = "dumpsys package " + package_name
        std_result, std_error = ADBUtil.execute_shell(serial, command, True, True)
        if key_word is None:
            return std_result
        try:
            for line in std_result.split("\n"):
                if key_word in line:
                    return line
        except Exception as why:
            print("get_information_of_installed_package error: ", why)
            return ""
        print("get_information_of_installed_package failed: no message match ", key_word)
        return ""

    @staticmethod
    def get_installed_package_version_code(serial, package_name):
        information = ADBUtil.get_information_of_installed_package(serial, package_name, "versionCode")
        if information != "":
            return int(information.split("versionCode=")[1].split()[0])
        print("get_installed_package_version_code failed")
        return 0

    @staticmethod
    def get_installed_package_version_name(serial, package_name):
        information = ADBUtil.get_information_of_installed_package(serial, package_name, "versionName")
        if information != "":
            return information.split("versionName=")[1].split()[0]
        print("get_installed_package_version_name failed")
        return ""

    @staticmethod
    def broadcast_action(serial, action_name, flag=None):
        LogUtil.log_start("broadcast_action: " + action_name)
        flag = " -f {}".format(flag) if flag is not None else ""
        command = "am broadcast -a {}{}".format(action_name, flag)
        ADBUtil.execute_shell(serial, command, output=True)
        LogUtil.log_end("broadcast_action: " + action_name)

    @staticmethod
    def wait_for_device(serial):
        LogUtil.log_start("wait_for_device")
        ADBUtil.execute_adb_command(serial, "wait-for-device")
        LogUtil.log_end("wait_for_device")

    @staticmethod
    def wait_for_reboot_complete(serial):
        while True:
            status = ADBUtil.get_prop(serial, "sys.boot_completed")
            if "1" in status and len(status.strip("\n").strip()) == 1:
                print("boot completed")
                break
            else:
                print("boot not completed wait,after five seconds check")
                time.sleep(5)

    @staticmethod
    def wait_and_check_is_in_oobe(serial, wait_sec=60, wait_gap_sec=5):
        while wait_sec > 0:
            result = ADBUtil.is_in_oobe(serial)
            if result:
                return True
            else:
                time.sleep(wait_gap_sec)
                wait_sec -= wait_gap_sec
        return False

    @staticmethod
    def is_in_page_of_package(serial, package_name):
        command = "dumpsys window"
        std_out, std_err = ADBUtil.execute_shell(serial, command, True, True)
        try:
            for line in std_out.split("\n"):
                if "mFocusedApp" in line:
                    return package_name in line
        except Exception as why:
            print("is_in_page_of_package check error: ", why)
            return False
        print("is_in_page_of_package: not in system")
        return False

    @staticmethod
    def is_in_oobe(serial):
        in_miui_oobe = ADBUtil.is_in_page_of_package(serial, "com.android.provision")
        in_google_oobe = ADBUtil.is_in_page_of_package(serial, "com.google.android.setupwizard")
        return in_miui_oobe or in_google_oobe

    @staticmethod
    def wait_for_enter_system(serial):
        while True:
            std_result, std_error = ADBUtil.execute_shell(serial, "dumpsys window", True, True)
            for line in std_result.split("\n"):
                if "mFocusedApp=" in line and "mFocusedApp=null" not in line:
                    return True
            time.sleep(5)

    @staticmethod
    def power_on(serial):
        command = "input keyevent 224"
        ADBUtil.execute_shell(serial, command)

    @staticmethod
    def take_screenshot(serial, out_put_file_path):
        ADBUtil.power_on(serial)
        ADBUtil.root_and_remount(serial)
        ADBUtil.execute_shell(serial, "screencap -p {}".format(out_put_file_path), True)

    @staticmethod
    def take_ui_layout(serial, out_put_file_path):
        ADBUtil.power_on(serial)
        ADBUtil.root_and_remount(serial)
        ADBUtil.execute_shell(serial, "uiautomator dump {}".format(out_put_file_path), True)

    @staticmethod
    def execute_shell(serial, shell_command, output=False, quiet=False):
        command = "{} -s {} shell {}".format(adb, serial, shell_command)
        print (command)
        # UsbUtil.make_sure_usb_connected(serial)

        if not output:
            ShellUtil.execute_shell(command, output, quiet)
        else:
            std_result, std_error = ShellUtil.execute_shell(command, True, quiet)
            if ADBUtil.is_zygote_failed(std_error):
                print('execute_shell(): Error, zygote failed. try restart')
                # Restart zygote and try again if failed.
                ADBUtil.restart_zygote(serial)
                std_result, std_error = ShellUtil.execute_shell(command, True, quiet=False)
            return std_result, std_error

    @staticmethod
    def execute_adb_command(serial, command, output=False, quiet=False):
        command = "{} -s {} {}".format(adb, serial, command)
        print (command)
        UsbUtil.make_sure_usb_connected(serial)
        return ShellUtil.execute_shell(command, output, quiet)

    @staticmethod
    def silence_and_disable_notification_in_device(serial):
        ADBUtil.root_and_remount(serial)
        ADBUtil.execute_shell(serial, "settings put global policy_control immersive.full=*", output=True)
        ADBUtil.execute_shell(serial, "pm disable com.android.systemui", output=True)
        ADBUtil.execute_shell(serial, "input keyevent 164", output=True)  # silence device
        pass

    @staticmethod
    def get_process_id_by_name(serial, process_name):
        std_out_1, std_err_1 = ADBUtil.execute_shell(serial, "ps", True, True)
        std_out_2, std_err_2 = ADBUtil.execute_shell(serial, "ps -A", True, True)
        process_info_1 = str(std_out_1).split("\n")
        process_info_2 = str(std_out_2).split("\n")
        process_info_all = set(process_info_1 + process_info_2)
        for process in process_info_all:
            if process_name in process:
                process_id = process.split()[1]
                print("process name: {} | process id: {}".format(process_name, process_id))
                return process_id
        print("get_process_id_by_name failed: not found {}".format(process_name))
        return None

    @staticmethod
    def get_date_time(serial):
        command = "date '+%Y-%m-%d\ %H:%M:%S'"
        std_out, std_err = ADBUtil.execute_shell(serial, command, True)
        if std_out is not None and len(std_out) != 0:
            return std_out.rstrip() + ".0"
        else:
            return None

    @staticmethod
    def check_package_exist(serial, package):
        return ADBUtil.is_package_installed(serial, package)

    @staticmethod
    def is_package_installed(serial, package):
        version_code = ADBUtil.get_installed_package_version_code(serial, package)
        return version_code > 0

    @staticmethod
    def get_apk_file_path(serial, package_name):
        if serial == "" or package_name == "":
            raise Exception("Parameter error: serial and package_name shouldn't be \"\" !")
        std_out, std_err = ADBUtil.execute_shell(serial, "pm path %s" % package_name, output=True)
        # pm path com.android.thememanager
        # Will get response as following:
        # package:/data/app/com.android.thememanager-8_76_QtAZedbweCb3xwKDA==/base.apk
        cmd_ret = std_out.strip()
        try:
            return cmd_ret[cmd_ret.find('/'):]
        except Exception as why:
            print("get_apk_file_path error: ", why)
            return ""

    @staticmethod
    def clear_package_data(serial, package_name):
        ADBUtil.rm(serial, "/data/data/{}".format(package_name))

    @staticmethod
    def do_uninstall(serial, package_name):
        apk_file_path = ADBUtil.get_apk_file_path(serial, package_name)
        ADBUtil.rm(serial, apk_file_path)

    @staticmethod
    def uninstall(serial, package_name):
        LogUtil.log_start("uninstall")
        if not ADBUtil.is_package_installed(serial, package_name):
            return True
        ADBUtil.root_and_remount(serial)
        ADBUtil.do_uninstall(serial, package_name)
        ADBUtil.clear_package_data(serial, package_name)
        ADBUtil.reboot(serial)
        rst = not ADBUtil.is_package_installed(serial, package_name)
        LogUtil.log_end("uninstall: {} :".format(str(rst)))
        return rst

    @staticmethod
    def try_uninstall(serial, package_name, try_times=3):
        while try_times > 0:
            rst = ADBUtil.uninstall(serial, package_name)
            if rst:
                return True
            else:
                try_times -= 1
        return False

    @staticmethod
    def is_zygote_failed(error_msg):
        return ('Can\'t find service' in error_msg)

    @staticmethod
    def restart_zygote(serial):
        print ('restart_zygote()')
        ADBUtil.execute_shell(serial, 'start', output=True)
        time.sleep(120)

    @staticmethod
    def check_zygote_ready(serial):
        std_out, std_err = ADBUtil.execute_shell(serial, 'dumpsys window | grep mFocus', output=True)
        if ADBUtil.is_zygote_failed(std_err):
            print ('check_zygote_ready(): Fail to execute commands, try re-start zygote')
            ADBUtil.restart_zygote(serial)

