from global_ci_util.fds.object_sync_util import ObjectSyncUtil

PRESETTING_DOWNLOAD_BUCKET = "app.presetting"
PRESETTING_APK_NAME = "app-debug.apk"
PRESETTING_APK_NUMBER = 2


class PreSettingApkSyncUtil(ObjectSyncUtil):
    def __init__(self, access_key, access_secret):
        ObjectSyncUtil.__init__(self, access_key, access_secret, PRESETTING_DOWNLOAD_BUCKET,
                                PRESETTING_APK_NUMBER,
                                PRESETTING_APK_NAME)
        pass
