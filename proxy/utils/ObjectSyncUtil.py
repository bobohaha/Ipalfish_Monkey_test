import os.path
from proxy.utils.FdsUtil import FdsUtil


class ObjectSyncUtil(FdsUtil):
    _download_bucket = ""
    _object_prefixes = ""
    _object_local_file_name = ""
    _object_specific_name = ""
    _object_name_keyword = ""
    _object_number = 0

    def __init__(self, download_bucket, object_number, object_local_file_name,
                 object_prefixes="", object_name_keyword="", object_specific_name=""):
        FdsUtil.__init__(self)

        self._download_bucket = download_bucket
        self._object_local_file_name = object_local_file_name
        self._object_number = object_number
        self._object_prefixes = object_prefixes
        self._object_name_keyword = object_name_keyword
        self._object_specific_name = object_specific_name
        pass

    def get_object_versions_online(self):
        return self.get_folders_names_in_bucket_in_dir(
            self._download_bucket,
            dir=self._object_prefixes)

    def get_object_newest_version_online(self):
        versions = self.get_object_versions_online()
        print versions
        return max(versions)

    def download_objects_with_version(self, version, file_download_path='./'):
        dir = self._object_prefixes + str(version) + "/"
        self.download_objects_in_dir_in_bucket(self._download_bucket, self._object_number,
                                               dir=dir, file_download_path=file_download_path,
                                               download_file_name=self._object_specific_name,
                                               object_name_keyword=self._object_name_keyword)
        pass

    def download_newest_version_objects(self, file_download_path='./'):
        online_version = self.get_object_newest_version_online()
        local_version = self.get_local_object_version()
        if online_version > local_version:
            self.download_objects_with_version(online_version, file_download_path)
        return online_version, local_version

    def get_local_object_version(self):
        return self.get_local_apk_version(self._object_local_file_name)

    def get_local_apk_version(self, file_name, file_path='./'):
        file = file_path + file_name
        if not os.path.exists(file):
            return 0

        command = "aapt d badging " + file + " | grep 'pack' | cut -f3 -d' ' | cut -f2 -d'='"

        out_put = os.popen(command)
        out_put_version = out_put.read().split("'")[1].strip()
        return int(out_put_version)
