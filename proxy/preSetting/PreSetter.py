# coding=utf-8

from proxy.utils.PathUtil import PathUtil
from proxy.utils.LogUtil import LogUtil
from proxy.usb.UsbUtil import UsbUtil
from proxy.utils.ADBUtil import ADBUtil
from proxy.utils.ShellUtil import ShellUtil
from proxy.param import *
from proxy.params.CaseName import *
from proxy.utils.AndroidJUnitRunnerUtil import AndroidJUnitRunnerUtil
from PreSettingApkSyncUtil import *
from LocalResourcesSyncUtil import *

import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class PreSetter:
    PROJECT_NAME = "PreSetter"

    PRESETTING_PKG = "com.mi.globalAutoTestTool.sanityCheck.test"
    PRESETTING_CLASS = "com.mi.globalAutoTestTool.sanityCheck.appPreSetting."

    rst = None
    rstFileName = "PreSetter.txt"
    monkey_resource_path = "/monkey_test_resources"
    usr_home = os.path.expanduser('~')
    device_home = "/sdcard"
    resource_pc_path = usr_home + monkey_resource_path
    resource_device_path = device_home + monkey_resource_path

    def __init__(self, serial, out_path, package_name):
        self._device_serial = serial
        self._log_out_path = out_path
        self._package_name_arr = package_name.split(",")
        pass

    def install_downloaded_apk(self):
        LogUtil.log_start("install_downloaded_apk")
        UsbUtil.make_sure_usb_connected(self._device_serial, "0")
        self.rst = ADBUtil.try_install(self._device_serial, "./app-debug.apk")
        if self.rst:
            self.rst = ADBUtil.try_install(self._device_serial, "./app-debug-androidTest.apk")
        LogUtil.log_end("install_downloaded_apk")
        pass

    def download_or_upgrade_apk(self):
        LogUtil.log_start("download_or_upgrade_apk")
        _PathUtil = PathUtil(__file__)
        _PathUtil.chdir_here()
        if not os.path.exists(self.PROJECT_NAME):
            os.mkdir(self.PROJECT_NAME)
        _PathUtil.chdir(self.PROJECT_NAME)

        online_version, local_version = PreSettingApkSyncUtil().download_newest_version_objects()
        LogUtil.log("online_version: " + str(online_version))
        LogUtil.log("local_version: " + str(local_version))
        LogUtil.log_end("download_or_upgrade_apk")

    def run_presetting_ui(self):
        LogUtil.log_start("run_presetting")
        preset_classes = self.get_preset_classes()
        for class_name in preset_classes:
            class_name = self.PRESETTING_CLASS + class_name
            self.rst = self.run_android_junit_runner(class_name)
            if self.rst is not True:
                break
        self.move_result()
        LogUtil.log_start("run_presetting")

    def run_specific_set(self, package=None):
        if package is not None:
            specific_settings = {
                PackageName.MUSIC: "music_specific_set"
            }
            if package in specific_settings.keys():
                method = getattr(self, specific_settings[package])
                return method
            else:
                print(package + " no specific setting!!")
                return None
        else:
            need_local_resource = False
            for package_name in self._package_name_arr:
                method = self.run_specific_set(package_name)
                if method is not None:
                    method()

                if package_name in PACKAGE_NEED_LOCAL_RESOURCE:
                    need_local_resource = True

            if need_local_resource:
                self.download_and_push_resources()
            else:
                print str(self._package_name_arr) + " not need local resources"
        pass

    def download_and_push_resources(self):
        LogUtil.log_start("download_and_push_resources")
        self.download_resources()
        self.fix_resource_name()
        self.push_resources()
        LogUtil.log_end("download_and_push_resources")

    def download_resources(self):
        if not os.path.exists(self.resource_pc_path):
            os.mkdir(self.resource_pc_path)

        files_num = len([x for (_, _, files) in os.walk(self.resource_pc_path) for x in files])
        print "resource_files_num: " + str(files_num)
        if files_num != LOCAL_RESOURCES_NUMBER:
            os.system('rm -rf ' + self.resource_pc_path)
            os.mkdir(self.resource_pc_path)
            LocalResourcesSyncUtil().download_objects_in_bucket_root(self.resource_pc_path)

    def fix_resource_name(self):
        unexpected_name_substring = [" ", "-", "\(", "\)", "（", "）", "《", "》","\&"]
        target_substring = '_'
        for sub in unexpected_name_substring:
            ShellUtil.rename_sub_string(sub, target_substring, self.resource_pc_path, "*")

    def push_resources(self):
        ADBUtil.rm(self._device_serial, self.resource_device_path)
        for (root, _, files) in os.walk(self.resource_pc_path):
            if not root.endswith("/"):
                root += "/"

            for f in files:
                file_path = root + f
                ADBUtil.push(self._device_serial, file_path, self.resource_device_path)

    def music_specific_set(self):
        LogUtil.log_start("music_specific_set")
        ADBUtil.root_and_remount(self._device_serial)
        ADBUtil.execute_shell(self._device_serial, "touch sdcard/Download/global_music_ind")
        ADBUtil.set_prop(self._device_serial, "log.tag.MediaPlaybackServicePro", "V")
        ADBUtil.set_prop(self._device_serial, "log.tag.AsyncServiceProxy", "V")
        LogUtil.log_end("music_specific_set")

    def remove_accounts(self):
        self.run_android_junit_runner(REMOVE_ACCOUNT)
        pass

    def get_result(self):
        return self.rst

    def get_preset_classes(self):
        preset_classes = [PRESETTING_DEFAULT_CASE_NAME]
        for _package_name in self._package_name_arr:
            if _package_name in PRESETTING_CASE_PACKAGE.keys():
                preset_classes.append(PRESETTING_CASE_PACKAGE[_package_name])
        return preset_classes

    def run_android_junit_runner(self, class_name, max_try=3):
        rst = None
        for _ in range(0, max_try):
            if rst is None:
                UsbUtil.make_sure_usb_connected(self._device_serial, "0")
                AndroidJUnitRunnerUtil.run_adb_command_output(self._device_serial,
                                                              class_name,
                                                              self.PRESETTING_PKG,
                                                              self.rstFileName)
            else:
                break
            rst = AndroidJUnitRunnerUtil.analysis_instrument_run_result(self.rstFileName)
        if rst is None:
            rst = False
        return rst

    def move_result(self):
        LogUtil.log_start("move_result")

        command = "adb -s " + self._device_serial + " root"
        os.system(command)
        print command

        command = "mkdir -p " + self._log_out_path + "/com.mi.globalAutoTestTool.sanityCheck/cache"
        print command
        os.system(command)

        command = "adb -s " + self._device_serial + " pull /data/user/0/com.mi.globalAutoTestTool" \
                                                    ".sanityCheck/cache/ " \
                  + self._log_out_path + "/com.mi.globalAutoTestTool.sanityCheck/"
        print command
        os.system(command)

        LogUtil.log_end("move_result")

    def clear_pkg_cache_in_device(self):
        package_name = PreSetter.PRESETTING_PKG.split(".test")[0]
        ADBUtil.clear_pkg_cache(self._device_serial, package_name)
