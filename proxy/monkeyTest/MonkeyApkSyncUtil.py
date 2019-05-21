from global_ci_util.fds import ObjectSyncUtil
from ..config.account import *

MonkeyTestApkNumber = 2
MonkeyTestApkLocalName = "monkey_test_package.apk"
MonkeyTestBucketName = "auto.test.apk"


class MonkeyApkSyncUtil(ObjectSyncUtil):
    def __init__(self, packages):
        prefixes = packages + "/"
        ObjectSyncUtil.__init__(self, fds_access_key, fds_access_secret, MonkeyTestBucketName,
                                MonkeyTestApkNumber,
                                MonkeyTestApkLocalName,
                                object_prefixes=prefixes)
        pass
