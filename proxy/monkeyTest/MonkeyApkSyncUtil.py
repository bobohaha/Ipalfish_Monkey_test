from proxy.utils.ObjectSyncUtil import ObjectSyncUtil

MonkeyTestApkNumber = 2
MonkeyTestApkLocalName = "monkey_test_package.apk"
MonkeyTestBucketName = "auto.test.apk"


class MonkeyApkSyncUtil(ObjectSyncUtil):
    def __init__(self, packages):
        prefixes = packages + "/"
        ObjectSyncUtil.__init__(self, MonkeyTestBucketName,
                                MonkeyTestApkNumber,
                                MonkeyTestApkLocalName,
                                object_prefixes=prefixes)
        pass
