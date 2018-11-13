from proxy.utils.ObjectSyncUtil import ObjectSyncUtil


SYSOPT_DOWNLOAD_BUCKET = "sysopt"
SYSOPT_APK_NAME = "SYSOPT.apk"
SYSOPT_APK_NAME_KEYWORD = "release"
SYSOPT_APK_NUMBER = 2
SYSOPT_PACKAGE_NAME = "com.miui.sysopt"
SYSOPT_ORIGION_VERSION = 1


class SysoptApkSyncUtil(ObjectSyncUtil):

    def __init__(self):
        ObjectSyncUtil.__init__(self, SYSOPT_DOWNLOAD_BUCKET,
                                SYSOPT_APK_NUMBER,
                                SYSOPT_APK_NAME,
                                object_prefixes='',
                                object_name_keyword=SYSOPT_APK_NAME_KEYWORD,
                                object_specific_name=SYSOPT_APK_NAME)
        pass
