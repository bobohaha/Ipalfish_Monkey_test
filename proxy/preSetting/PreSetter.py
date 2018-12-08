from proxy.utils.PathUtil import PathUtil
from proxy.utils.LogUtil import LogUtil
from proxy.usb.UsbUtil import UsbUtil
from proxy.utils.ADBUtil import ADBUtil
from proxy.param import *
from proxy.params.CaseName import *
from proxy.utils.AndroidJUnitRunnerUtil import AndroidJUnitRunnerUtil
from PreSettingApkSyncUtil import *
from LocalResourcesSyncUtil import *

import os


class PreSetter:
    PROJECT_NAME = "PreSetter"

    PRESETTING_PKG = "com.mi.globalAutoTestTool.sanityCheck.test"
    PRESETTING_CLASS = "com.mi.globalAutoTestTool.sanityCheck.appPreSetting."

    rst = None
    rstFileName = "PreSetter.txt"

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

    def run_presetting(self):
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
        pass

    def download_and_push_resources(self):
        usr_home = os.path.expanduser('~')
        resource_path = usr_home + "/monkey_test_resources/"
        if not os.path.exists(resource_path):
            os.mkdir(resource_path)

        files_num = len([x for x in os.listdir(resource_path) if os.path.isfile(x)])
        if files_num <= LOCAL_RESOURCES_NUMBER:
            LocalResourcesSyncUtil().download_objects_in_bucket_root(resource_path)

        for f in os.listdir(resource_path):
            if os.path.isfile(f):
                print f
                # ADBUtil.push(self._device_serial, f)

    def music_specific_set(self):
        ADBUtil.root_and_remount(self._device_serial)
        ADBUtil.execute_shell(self._device_serial, "touch sdcard/Download/global_music_ind")
        ADBUtil.set_prop(self._device_serial, "log.tag.MediaPlaybackServicePro", "V")
        ADBUtil.set_prop(self._device_serial, "log.tag.AsyncServiceProxy", "V")
        pass

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
