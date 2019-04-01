from proxy.utils.ADBUtil import ADBUtil


class PropUtil:

    def __init__(self):
        pass

    PROP_DEVICE_PRODUCT = ["ro.build.product"]
    PROP_MOD_DEVICE = ["ro.product.mod_device", "ro.product.device"]
    PROP_ROM_VERSION = ["ro.build.version.incremental"]
    PROP_ANDROID_VERSION = ["ro.build.version.release"]
    PROP_ROM_SIGNATURE = ["ro.build.tags"]

    @staticmethod
    def get_device_name(serial):
        for prop in PropUtil.PROP_DEVICE_PRODUCT:
            result = ADBUtil.get_prop(serial, prop)
            if result:
                return result
        raise PropUtil.PropertyNotFound("Get device name error")

    @staticmethod
    def get_mod_device_name(serial):
        for prop in PropUtil.PROP_MOD_DEVICE:
            result = ADBUtil.get_prop(serial, prop)
            if result:
                return result
        raise PropUtil.PropertyNotFound("Get mod device name error")

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

    @staticmethod
    def get_device_rom_signature(serial):
        for prop in PropUtil.PROP_ROM_SIGNATURE:
            result = ADBUtil.get_prop(serial, prop)
            if result:
                return result
        raise PropUtil.PropertyNotFound("Get rom signature error")

    class PropertyNotFound(Exception):
        pass
