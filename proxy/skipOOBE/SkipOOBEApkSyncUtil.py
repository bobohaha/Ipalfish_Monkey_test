from proxy.utils.ObjectSyncUtil import ObjectSyncUtil

SKIP_OOBE_DOWNLOAD_BUCKET = "global"
SKIP_OOBE_OBJECTS_PREFIXES = "skipOOBE/"
SKIP_OOBE_APK_NAME = "app-debug.apk"
SKIP_OOBE_APK_NUMBER = 2


class SkipOOBEApkSyncUtil(ObjectSyncUtil):
    def __init__(self):
        ObjectSyncUtil.__init__(self, SKIP_OOBE_DOWNLOAD_BUCKET,
                                SKIP_OOBE_APK_NUMBER,
                                SKIP_OOBE_APK_NAME,
                                object_prefixes=SKIP_OOBE_OBJECTS_PREFIXES)
        pass
