from proxy.utils.ObjectSyncUtil import ObjectSyncUtil

LOCAL_RESOURCES_DOWNLOAD_BUCKET = "test.resources"
LOCAL_RESOURCES_LOCAL_NAME = "NONE"
LOCAL_RESOURCES_NUMBER = 60


class LocalResourcesSyncUtil(ObjectSyncUtil):
    def __init__(self):
        ObjectSyncUtil.__init__(self, LOCAL_RESOURCES_DOWNLOAD_BUCKET,
                                LOCAL_RESOURCES_NUMBER,
                                LOCAL_RESOURCES_LOCAL_NAME)
        pass

    def download_objects_in_bucket_root(self, file_download_path):
        if not file_download_path.endswith("/"):
            file_download_path += "/"
        self.download_objects_in_dir_in_bucket(LOCAL_RESOURCES_DOWNLOAD_BUCKET, LOCAL_RESOURCES_NUMBER, dir='',
                                               file_download_path=file_download_path, download_file_name=None,
                                               object_name_keyword="")
