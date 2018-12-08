from proxy.utils.PathUtil import PathUtil
from proxy.utils.LogUtil import LogUtil
from proxy.usb.UsbUtil import UsbUtil
from proxy.utils.ADBUtil import ADBUtil
from SysoptApkSyncUtil import *

import os


class DeviceRecover:
    PROJECT_NAME = "RecoverDevice"
    RECOVER_BROADCAST_ACTION = "com.omni.recover.build_in.app"

    rst = None
    rstFileName = "recoverDevice.txt"

    _device_serial = ""

    def __init__(self, serial):
        self._device_serial = serial
        self.sysopt_online_version = SysoptApkSyncUtil().get_object_newest_version_online()
        pass

    def wait_for_device_ready(self):
        ADBUtil.wait_for_device(self._device_serial)
        UsbUtil.make_sure_usb_connected(self._device_serial, "0")
        ADBUtil.wait_for_reboot_complete(self._device_serial)
        ADBUtil.wait_for_enter_system(self._device_serial)

    def reboot_device(self):
        UsbUtil.make_sure_usb_connected(self._device_serial, "0")
        ADBUtil.reboot(self._device_serial)
        self.wait_for_device_ready()
        pass

    def download_install_apk_and_make_sure_usb(self):
        self.download_or_upgrade_apk()
        UsbUtil.make_sure_usb_connected(self._device_serial, "0")
        self.install_downloaded_apk()
        self.wait_for_device_ready()
        pass

    def download_or_upgrade_apk(self):
        LogUtil.log_start("download_or_upgrade_apk")

        _PathUtil = PathUtil(__file__)
        _PathUtil.chdir_here()
        if not os.path.exists(DeviceRecover.PROJECT_NAME):
            os.mkdir(DeviceRecover.PROJECT_NAME)

        _PathUtil.chdir(DeviceRecover.PROJECT_NAME)

        self.sysopt_online_version, local_version = SysoptApkSyncUtil().download_newest_version_objects()
        LogUtil.log("online_version: " + str(self.sysopt_online_version))
        LogUtil.log("local_version: " + str(local_version))
        LogUtil.log_end("download_or_upgrade_apk")

    def install_downloaded_apk(self):
        LogUtil.log_start("install_downloaded_apk")
        ADBUtil.install(
            self._device_serial, SYSOPT_APK_NAME)
        LogUtil.log_end("install_downloaded_apk")
        pass

    def is_sysopt_version_newest(self):
        current_version = ADBUtil.get_installed_package_version(self._device_serial,
                                                                SYSOPT_PACKAGE_NAME)
        LogUtil.log("check_sysopt_version::current: " + current_version)
        if current_version is None or current_version == "":
            return False
        return int(current_version.strip()) == self.sysopt_online_version

    def recover_device(self, max_try=3):
        LogUtil.log_start("recover_device")
        for _ in range(0, max_try):

            if self.rst is False:
                self.reboot_device()
                self.rst = None

            if self.rst is None:
                self.do_recover_device()

            if self.rst is True:
                break
        LogUtil.log_end("recover_device")

    def do_recover_device(self):
        LogUtil.log_start("do_recover_device")
        if not self.is_sysopt_version_newest():
            self.download_install_apk_and_make_sure_usb()
        ADBUtil.broadcast_action(self._device_serial, self.RECOVER_BROADCAST_ACTION)
        self.wait_for_device_ready()
        self.rst = ADBUtil.wait_and_check_is_in_oobe(self._device_serial)
        LogUtil.log_end("do_recover_device")

    def get_result(self):
        return self.rst
