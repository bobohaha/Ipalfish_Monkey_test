from global_ci_util import ADBUtil

PROP_DEVICE_PRODUCT = "ro.build.product"
PROP_MOD_DEVICE = ["ro.product.mod_device", "ro.product.device"]
PROP_ROM_VERSION = "ro.build.version.incremental"
PROP_ANDROID_VERSION = "ro.build.version.release"
PROP_ROM_SIGNATURE = "ro.build.tags"


def get_device_name(serial):
    result = try_get_prop(serial, PROP_DEVICE_PRODUCT)
    if result:
        return result
    raise PropertyNotFound("get_device_name error")


def get_mod_device_name(serial):
    for prop in PROP_MOD_DEVICE:
        result = try_get_prop(serial, prop)
        if result:
            return result
    raise PropertyNotFound("get_mod_device_name error")


def get_rom_version(serial):
    result = try_get_prop(serial, PROP_ROM_VERSION)
    if result:
        return result
    raise PropertyNotFound("get_rom_version error")


def get_android_version(serial):
    result = try_get_prop(serial, PROP_ANDROID_VERSION)
    if result:
        return result
    raise PropertyNotFound("get_android_version error")


def get_device_rom_signature(serial):
    result = try_get_prop(serial, PROP_ROM_SIGNATURE)
    if result:
        return result
    raise PropertyNotFound("get_device_rom_signature error")


def try_get_prop(serial, prop, try_time=3):
    result = None
    while try_time > 0:
        print('getprop '+prop)
        result = ADBUtil.get_prop(serial, prop)
        if result:
            return result
        try_time -= 1
    return result


class PropertyNotFound(Exception):
    pass