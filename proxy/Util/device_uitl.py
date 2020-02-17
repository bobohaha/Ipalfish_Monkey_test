from proxy.Util.adb_util import ADBUtil


class DeviceUtil:
    def __init__(self):
        pass

    @staticmethod
    def reboot_device(_serial):
        ADBUtil.reboot(_serial)
        pass

    @staticmethod
    def clear_device_log(_serial, _out_path):
        ADBUtil.rm(_serial, _out_path)
        pass