from proxy.utils.ADBUtil import ADBUtil


class PropUtil:

    PROP_DEVICE_PRODUCT = ["ro.build.product"]
    PROP_ROM_VERSION = ["ro.build.version.incremental"]

    @staticmethod
    def get_device_name(serial):
        for prop in PropUtil.PROP_DEVICE_PRODUCT:
            result = ADBUtil.get_prop(serial, prop)
            if result:
                break
        return result

    @staticmethod
    def get_rom_version(serial):
        for prop in PropUtil.PROP_ROM_VERSION:
            result = ADBUtil.get_prop(serial, prop)
            if result:
                break
        return result