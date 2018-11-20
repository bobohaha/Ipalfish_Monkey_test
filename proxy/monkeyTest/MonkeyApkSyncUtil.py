from proxy.utils.ObjectSyncUtil import ObjectSyncUtil

MonkeyTestApkNumber = 1
MonkeyTestApkLocalName = "monkey_test_package.apk"


class MonkeyApkSyncUtil(ObjectSyncUtil):
    def __init__(self, download_bucket):
        ObjectSyncUtil.__init__(self, download_bucket,
                                MonkeyTestApkNumber,
                                MonkeyTestApkLocalName,
                                object_specific_name=MonkeyTestApkLocalName)
        pass
