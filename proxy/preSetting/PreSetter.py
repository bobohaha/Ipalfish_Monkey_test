from proxy.utils.PathUtil import PathUtil
from proxy.utils.LogUtil import LogUtil
from proxy.usb.UsbUtil import UsbUtil
from proxy.utils.ADBUtil import ADBUtil
from proxy import param
from proxy.utils.AndroidJUnitRunnerUtil import AndroidJUnitRunnerUtil
from PreSettingApkSyncUtil import *

import os
import re


class PreSetter:
    PROJECT_NAME = "PreSetter"

    PRESETTING_PKG = "com.mi.globalAutoTestTool.sanityCheck.test"
    PRESETTING_CLASS = "com.mi.globalAutoTestTool.sanityCheck.appPreSetting."

    rst = None
    rstFileName = "PreSetter.txt"

    _device_serial = ""
    _log_out_path = ""

    _package_name = ""

    def __init__(self, serial, out_path, package_name):
        self._device_serial = serial
        self._log_out_path = out_path
        self._package_name = package_name
        pass

    def install_downloaded_apk(self):
        LogUtil.log_start("install_downloaded_apk")
        UsbUtil.make_sure_usb_connected(self._device_serial, "0")
        ADBUtil.install_and_async_monitor_google_dialog_to_workaround(
            self._device_serial, "./app-debug.apk")
        ADBUtil.install_and_async_monitor_google_dialog_to_workaround(
            self._device_serial, "./app-debug-androidTest.apk")
        LogUtil.log_end("install_downloaded_apk")
        pass

    def download_or_upgrade_apk(self):
        LogUtil.log_start("download_or_upgrade_apk")

        _PathUtil = PathUtil(__file__)
        _PathUtil.chdir_here()
        if not os.path.exists(PreSetter.PROJECT_NAME):
            os.mkdir(PreSetter.PROJECT_NAME)

        _PathUtil.chdir(PreSetter.PROJECT_NAME)

        online_version, local_version = PreSettingApkSyncUtil().download_newest_version_objects()
        LogUtil.log("online_version: " + str(online_version))
        LogUtil.log("local_version: " + str(local_version))
        LogUtil.log_end("download_or_upgrade_apk")

    def run_presetting(self):
        LogUtil.log_start("run_presetting")

        MAX_ROUND_COUNT = 3
        for _ in range(0, MAX_ROUND_COUNT):

            if self.rst is None:
                UsbUtil.make_sure_usb_connected(self._device_serial, "0")
                self.run_android_junit_runner()
            else:
                break

            self.analyze_result()

        LogUtil.log_start("run_presetting")

    def analyze_result(self):
        LogUtil.log("analyze_result")

        _PathUtil = PathUtil(__file__)
        _PathUtil.chdir_here()
        _PathUtil.chdir(PreSetter.PROJECT_NAME)

        if os.path.exists("%s" % self.rstFileName) is False:
            LogUtil.log("file isn't exist.")
            return None

        for line in open("%s" % self.rstFileName, 'r'):
            LogUtil.log(line)

            if re.search("Failure", line):
                LogUtil.log("Presetting run failure")
                self.rst = False
                break

            if re.search("OK", line):
                LogUtil.log("Presetting run OK")
                self.rst = True
                break

        if self.rst is None:
            LogUtil.log("Presetting run  unfinished")

    def get_result(self):

        if self.rst is None:
            return False

        return self.rst

    def get_class_name(self):
        if self._package_name in param.PRESETTING_CASE_PACKAGE.keys():
            return param.PRESETTING_CASE_PACKAGE[self._package_name]
        return param.PRESETTING_DEFAULT_CASE_NAME

    def run_android_junit_runner(self):
        class_name = self.get_class_name()
        class_name = self.PRESETTING_CLASS + class_name

        AndroidJUnitRunnerUtil.run_adb_command_output(self._device_serial,
                                                      class_name,
                                                      self.PRESETTING_PKG,
                                                      self.rstFileName)

        pass
