import os

from proxy.utils.LogUtil import LogUtil
from proxy.utils.PathUtil import PathUtil
from proxy.utils.GitUtil import GitUtil


class UsbUtil:

    PREPARE_GIT_SITE = "git@v9.git.n.xiaomi.com:GlobalAutomationTest_Omni/ResetUsb.git"
    PREPARE_PROJECT_NAME = "ResetUsb"

    def __init__(self):
        pass

    @staticmethod
    def make_sure_usb_connected(serial, wait_time):
        LogUtil.log_start("waitForAdbConnected")

        _PathUtil = PathUtil(__file__)
        _PathUtil.chdir_here()

        GitUtil.clone_if_no_exist(UsbUtil.PREPARE_GIT_SITE, UsbUtil.PREPARE_PROJECT_NAME)

        _PathUtil.chdir(UsbUtil.PREPARE_PROJECT_NAME)

        command = "python " + os.getcwd() + "/checkStateAndResetUsb.py " + serial + " " + str(wait_time)

        print command
        os.system(command)

        _PathUtil.back()

        LogUtil.log_end("waitForAdbConnected")






