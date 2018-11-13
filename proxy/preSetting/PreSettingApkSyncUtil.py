from proxy.utils.ObjectSyncUtil import ObjectSyncUtil

PRESETTING_DOWNLOAD_BUCKET = "app.presetting"
PRESETTING_APK_NAME = "app-debug.apk"
PRESETTING_APK_NUMBER = 2


class PreSettingApkSyncUtil(ObjectSyncUtil):
    def __init__(self):
        ObjectSyncUtil.__init__(self, PRESETTING_DOWNLOAD_BUCKET,
                                PRESETTING_APK_NUMBER,
                                PRESETTING_APK_NAME)
        pass
