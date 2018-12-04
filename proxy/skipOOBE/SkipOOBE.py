from proxy.utils.PathUtil import PathUtil
from proxy.utils.GitUtil import GitUtil
from proxy.utils.GradleUtil import GradleUtil
from proxy.utils.LogUtil import LogUtil
from proxy.usb.UsbUtil import UsbUtil
from proxy.utils.ADBUtil import ADBUtil
from proxy import param
from proxy.utils.AndroidJUnitRunnerUtil import AndroidJUnitRunnerUtil
from SkipOOBEApkSyncUtil import SkipOOBEApkSyncUtil
from proxy.utils.PropUtil import PropUtil

import os
import re


class SkipOOBE:
    GIT_SITE = "git@v9.git.n.xiaomi.com:GlobalAutomationTest_Omni/SkipOOBE.git"
    PROJECT_NAME = "SkipOOBE"

    SKIPOOBE_PKG = "com.mi.globalAutoTestTool.skipOOBE.test"
    SKIPOOBE_CLASS = "com.mi.globalAutoTestTool.skipOOBE.V10.RobotManager"

    rst = None
    rstFileName = "skipOOBE.txt"

    _device_serial = ""
    _log_out_path = ""
    _rom_info = ""
    _device_name = ""

    _extra_params = {}

    def __init__(self, serial, out_path, param_dict, test_region_language):
        self._device_serial = serial
        self._log_out_path = out_path
        self._rom_info = param_dict
        self._extra_params = test_region_language
        self._device_name = PropUtil.get_device_name(serial)
        pass

    def generate_and_install_apk(self):
        self.generate_with_region_and_install_apk(None)
        pass

    def generate_with_region_and_install_apk(self, region):
        self.generate_apk_with_region(region)
        self.install_apk()
        pass

    def generate_and_install_apk_make_sure_usb(self):
        self.generate_with_region_and_install_apk_make_sure_usb(None)
        pass

    def generate_with_region_and_install_apk_make_sure_usb(self, region):
        self.generate_with_region_and_make_sure_usb(region)
        self.install_apk()
        pass

    def generate_and_make_sure_usb(self):
        self.generate_with_region_and_make_sure_usb(None)
        pass

    def generate_with_region_and_make_sure_usb(self, region):
        self.generate_apk_with_region(region)
        UsbUtil.make_sure_usb_connected(self._device_serial, "0")
        pass

    def generate_apk(self):
        self.generate_apk_with_region(None)
        pass

    def generate_apk_with_region(self, region):
        LogUtil.log_start("generate_apk_with_region")

        _PathUtil = PathUtil(__file__)
        _PathUtil.chdir_here()

        GitUtil.force_clone(SkipOOBE.GIT_SITE, SkipOOBE.PROJECT_NAME)

        GradleUtil.copy_properties_to(SkipOOBE.PROJECT_NAME)

        if region is not None:
            command = "echo %s > " % region + "./SkipOOBE/app/src/main/assets/Locale.txt"
            print command
            os.system(command)

        _PathUtil.chdir(SkipOOBE.PROJECT_NAME)

        GradleUtil.clean_assembledebug_assembleAndroidTest()

        LogUtil.log_end("generate_apk_with_region")

    def install_apk(self):
        LogUtil.log_start("install_apk")
        ADBUtil.install(self._device_serial, "./app/build/outputs/apk/debug/app-debug.apk")
        ADBUtil.install(self._device_serial,
                        "./app/build/outputs/apk/androidTest/debug/app-debug-androidTest.apk")
        pass

    def install_downloaded_apk(self):
        LogUtil.log_start("install_downloaded_apk")
        UsbUtil.make_sure_usb_connected(self._device_serial, "0")
        self.rst = ADBUtil.try_install(self._device_serial, "./app-debug.apk")
        if self.rst:
            self.rst = ADBUtil.try_install(self._device_serial, "./app-debug-androidTest.apk")
        LogUtil.log_end("install_downloaded_apk")

    def download_or_upgrade_apk(self):
        LogUtil.log_start("download_or_upgrade_apk")

        _PathUtil = PathUtil(__file__)
        _PathUtil.chdir_here()
        if not os.path.exists(SkipOOBE.PROJECT_NAME):
            os.mkdir(SkipOOBE.PROJECT_NAME)

        _PathUtil.chdir(SkipOOBE.PROJECT_NAME)

        online_version, local_version = SkipOOBEApkSyncUtil().download_newest_version_objects()
        LogUtil.log("online_version: " + str(online_version))
        LogUtil.log("local_version: " + str(local_version))
        LogUtil.log_end("download_or_upgrade_apk")

    def run_test(self):
        LogUtil.log_start("run_test")
        self.rst = None
        run_count_remain = 3
        while run_count_remain > 0:
            if self.rst is None:
                UsbUtil.make_sure_usb_connected(self._device_serial, "0")
                self.run_android_junit_runner()
                run_count_remain -= 1
            else:
                break
            self.analyze_result()
        LogUtil.log_end("run_test")

    def move_result(self):
        LogUtil.log_start("move_result")

        command = "adb -s " + self._device_serial + " root"
        os.system(command)
        print command

        command = "mkdir -p " + self._log_out_path + "/com.mi.globalAutoTestTool.skipOOBE/cache"
        print command
        os.system(command)

        command = "adb -s " + self._device_serial + " pull /data/user/0/com.mi.globalAutoTestTool" \
                                                    ".skipOOBE/cache/ " \
                  + self._log_out_path + "/com.mi.globalAutoTestTool.skipOOBE/"
        print command
        os.system(command)

        LogUtil.log_end("move_result")

    def analyze_result(self):
        LogUtil.log("analyze_result")

        _PathUtil = PathUtil(__file__)
        _PathUtil.chdir_here()
        _PathUtil.chdir(SkipOOBE.PROJECT_NAME)

        if os.path.exists("%s" % self.rstFileName) is False:
            LogUtil.log("file isn't exist.")
            return None

        for line in open("%s" % self.rstFileName, 'r'):
            LogUtil.log(line)

            if re.search("Failure", line):
                LogUtil.log("skipOOBE run failure")
                self.rst = False
                break

            if re.search("OK ", line):
                LogUtil.log("skipOOBE run OK")
                self.rst = True
                break

        if self.rst is None:
            LogUtil.log("skipOOBE run  unfinished")

    def get_result(self):

        if self.rst is None:
            return False

        return self.rst

    def make_sure_in_oobe(self):
        UsbUtil.make_sure_usb_connected(self._device_serial, "0")

        _PathUtil = PathUtil(__file__)
        if not os.path.exists("shell"):
            _PathUtil.chdir_here()

        command = "sh " + os.getcwd() + "/shell/waitToOOBE.sh " + self._device_serial
        print command
        os.system(command)

        if os.path.exists(SkipOOBE.PROJECT_NAME):
            _PathUtil.chdir(SkipOOBE.PROJECT_NAME)
        pass

    def run_android_junit_runner(self):
        if self._device_name in param.NEED_CONNECT_WIFI_DEVICE:
            self._extra_params.setdefault(param.IS_NEED_CONNECT_WIFI_KEY,
                                          param.IS_NEED_CONNECT_WIFI_VALUE)
            LogUtil.log("skipOOBE: " + self._device_name + " need connect wifi")

        AndroidJUnitRunnerUtil.run_adb_command_output_with_extra_param(self._device_serial,
                                                                       self.SKIPOOBE_CLASS,
                                                                       self.SKIPOOBE_PKG,
                                                                       self.rstFileName,
                                                                       self._extra_params)

        pass
