from global_ci_util.fds import ObjectSyncUtil
from ..config.account import *

MonkeyTestApkNumber = 2
MonkeyTestApkLocalName = "monkey_test_package.apk"
MonkeyTestBucketName = "auto.test.apk"
MonkeyTestBucketNameNewCI = "global.ci"


class MonkeyApkSyncUtil(ObjectSyncUtil):
    def __init__(self, packages, is_new_ci):
        prefixes = packages + "/"
        bucket_name = MonkeyTestBucketName
        if is_new_ci:
            prefixes = "daily/" + prefixes
            bucket_name = MonkeyTestBucketNameNewCI
        ObjectSyncUtil.__init__(self, fds_access_key, fds_access_secret, bucket_name,
                                MonkeyTestApkNumber,
                                MonkeyTestApkLocalName,
                                object_prefixes=prefixes)
        pass
