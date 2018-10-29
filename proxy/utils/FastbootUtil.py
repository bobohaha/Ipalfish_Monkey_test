import os
from proxy.utils.LogUtil import LogUtil

class FastbootUtil:

    @staticmethod
    def check_device_in_fastboot(serial):
        command = "fastboot devices | grep " + serial
        os.system(command)

        output = os.popen(command)
        text = output.read().strip()
        if len(text) > 1 :
            return True
        else:
            return False

    @staticmethod
    def reboot_to_bootloader(serial):
        LogUtil.log_start("reboot_to_bootloader")

        command = "fastboot -s " + serial + " reboot-bootloader"
        LogUtil.log(command)
        os.system(command)

        LogUtil.log_end("reboot_to_bootloader")

    @staticmethod
    def reboot(serial):
        LogUtil.log_start("reboot")

        command = "fastboot -s " + serial + " reboot"
        LogUtil.log(command)
        os.system(command)

        LogUtil.log_end("reboot")



