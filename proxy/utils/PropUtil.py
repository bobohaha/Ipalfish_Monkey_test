from proxy.utils.ADBUtil import ADBUtil


class PropUtil:

    def __init__(self):
        pass

    PROP_DEVICE_PRODUCT = ["ro.build.product"]
    PROP_ROM_VERSION = ["ro.build.version.incremental"]
    PROP_ANDROID_VERSION = ["ro.build.version.release"]

    @staticmethod
    def get_device_name(serial):
        for prop in PropUtil.PROP_DEVICE_PRODUCT:
            result = ADBUtil.get_prop(serial, prop)
            if result:
                return result
        raise PropUtil.PropertyNotFound("Get device name error")

    @staticmethod
    def get_rom_version(serial):
        for prop in PropUtil.PROP_ROM_VERSION:
            result = ADBUtil.get_prop(serial, prop)
            if result:
                return result
        raise PropUtil.PropertyNotFound("Get rom version error")

    @staticmethod
    def get_android_version(serial):
        for prop in PropUtil.PROP_ANDROID_VERSION:
            result = ADBUtil.get_prop(serial, prop)
            if result:
                return result
        raise PropUtil.PropertyNotFound("Get android version error")

    class PropertyNotFound(Exception):
        pass
