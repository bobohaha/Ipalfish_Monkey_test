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
        pass

    def reboot_device(self):
        UsbUtil.make_sure_usb_connected(self._device_serial, "0")
        ADBUtil.reboot(self._device_serial)
        ADBUtil.wait_for_device(self._device_serial)
        ADBUtil.wait_for_reboot_complete(self._device_serial)
        pass

    def download_install_apk_and_make_sure_usb(self):
        self.download_or_upgrade_apk()
        UsbUtil.make_sure_usb_connected(self._device_serial, "0")
        self.install_downloaded_apk()
        ADBUtil.wait_for_device(self._device_serial)
        ADBUtil.wait_for_reboot_complete(self._device_serial)
        pass

    def download_or_upgrade_apk(self):
        LogUtil.log_start("download_or_upgrade_apk")

        _PathUtil = PathUtil(__file__)
        _PathUtil.chdir_here()
        if not os.path.exists(DeviceRecover.PROJECT_NAME):
            os.mkdir(DeviceRecover.PROJECT_NAME)

        _PathUtil.chdir(DeviceRecover.PROJECT_NAME)

        online_version, local_version = SysoptApkSyncUtil().download_newest_version_objects()
        LogUtil.log("online_version: " + str(online_version))
        LogUtil.log("local_version: " + str(local_version))
        LogUtil.log_end("download_or_upgrade_apk")

    def install_downloaded_apk(self):
        LogUtil.log_start("install_downloaded_apk")
        ADBUtil.install_and_async_monitor_google_dialog_to_workaround(
            self._device_serial, SYSOPT_APK_NAME)
        LogUtil.log_end("install_downloaded_apk")
        pass

    def is_sysopt_version_new(self):
        current_version = ADBUtil.get_installed_package_version(self._device_serial,
                                                                SYSOPT_PACKAGE_NAME)
        LogUtil.log("check_sysopt_version::current: " + current_version)
        if current_version is None or current_version == "":
            return False

        return int(current_version.strip()) > SYSOPT_ORIGION_VERSION

    def recover_device(self):
        LogUtil.log_start("recover_device")
        self.reboot_device()

        if self.is_sysopt_version_new():
            ADBUtil.broadcast_action(self._device_serial, self.RECOVER_BROADCAST_ACTION)
        else:
            self.download_install_apk_and_make_sure_usb()
            self.recover_device()
        LogUtil.log_start("recover_device")
