from .log_util import LogUtil
import os


class UsbUtil:
    PREPARE_PROJECT_NAME = "gitResetUsb"

    def __init__(self):
        pass

    @staticmethod
    def make_sure_usb_connected(serial, wait_time="0"):
        LogUtil.log_start("waitForAdbConnected")

        is_find_device = (os.system('adb devices | grep %s' % serial) == 0)
        if is_find_device:
            LogUtil.log_end("waitForAdbConnected")
            return

        #global_ci_util.usb.check_state_and_reset_usb.run(serial, int(wait_time))

        LogUtil.log_end("waitForAdbConnected")

