from fds import FDSClientConfiguration, GalaxyFDSClient, GalaxyFDSClientException
import os
import time


class FdsUtil:
    ACCESS_KEY = "AKIAT3L6HCEBTONSSH"
    ACCESS_SECRET = "k97PskGi9CLX0Lw+vAi2VziiJxl4NljGAA1pAyb8"
    ENDPOINT = "cnbj1-fds.api.xiaomi.net"

    def __init__(self):
        self.fds_config = FDSClientConfiguration(enable_cdn_for_download=False,
                                                 enable_cdn_for_upload=False,
                                                 enable_https=True,
                                                 endpoint=FdsUtil.ENDPOINT)
        self.fds_client = GalaxyFDSClient(access_key=FdsUtil.ACCESS_KEY,
                                          access_secret=FdsUtil.ACCESS_SECRET,
                                          config=self.fds_config)
        pass

    def list_buckets(self):
        return self.fds_client.list_buckets()

    def does_bucket_exist(self, bucket_name):
        return self.fds_client.does_bucket_exist(bucket_name)

    def create_bucket(self, bucket_name):
        return self.fds_client.create_bucket(bucket_name)

    def delete_bucket(self, bucket_name):
        return self.fds_client.delete_bucket(bucket_name)

    def list_authorized_buckets(self):
        return self.fds_client.list_authorized_buckets()

    def list_objects(self, bucket_name, prefix='', delimiter=None, max_keys=None):
        return self.fds_client.list_objects(bucket_name, prefix, delimiter, max_keys)

    def list_all_objects(self, bucket_name, prefix='', delimiter=None):
        return self.fds_client.list_all_objects(bucket_name, prefix, delimiter)

    def get_folders_names_in_bucket_in_dir(self, bucket_name, dir=''):
        fds_objects_listing = self.list_objects(bucket_name, prefix=dir)
        object_versions = fds_objects_listing.common_prefixes
        version = []

        for index in range(0, len(object_versions)):
            fds_obj_version = object_versions[index]
            if not fds_obj_version.endswith("/"):
                fds_obj_version = fds_obj_version + "/"

            object_listing = self.list_objects(bucket_name, prefix=fds_obj_version)
            object_summary = object_listing.objects
            if len(object_summary) != 3:
                continue

            if isinstance(fds_obj_version, bytes):
                fds_obj_version = fds_obj_version.decode(encoding='utf-8')

            path = fds_obj_version.split("/")

            fds_obj_version = path[len(path)-2].strip()
            version.append(int(fds_obj_version))
        return version

    def generate_download_object_uri(self, bucket_name, object_name):
        return self.fds_client.generate_download_object_uri(bucket_name, object_name)

    def download_object_with_uri(self, uri, data_file, offset=0, length=-1):
        self.fds_client.download_object_with_uri(uri, data_file, offset, length)
        pass

    def download_object(self, bucket_name, object_name, data_file, offset=0, length=-1):
        self.fds_client.download_object(bucket_name, object_name, data_file, offset, length)
        pass

    def download_objects_in_dir_in_bucket(self, bucket_name, objects_num, dir='',
                                          file_download_path='./', download_file_name=None,
                                          object_name_keyword=""):
        objects_listing = self.list_objects(bucket_name, prefix=dir)
        if not objects_listing:
            raise Exception("Find objects online error")

        download_objects = objects_listing.objects

        download_objects_num = len(download_objects)

        if 0 <= objects_num+1 != download_objects_num:
            raise Exception("The num of objects online is error")

        if not os.path.exists(file_download_path):
            os.mkdir(file_download_path)

        for download_object in download_objects:
            if not download_object.object_name.endswith('/'):
                if download_file_name is not None and download_file_name is not '':
                    _download_file = file_download_path + str(download_file_name)
                else:
                    download_files = download_object.object_name.split("/")
                    _download_file = file_download_path + download_files[len(download_files) - 1]
                if object_name_keyword == "":
                    self.download_object(bucket_name, download_object.object_name, _download_file)
                elif object_name_keyword in download_object.object_name:
                    self.download_object(bucket_name, download_object.object_name, _download_file)

                times = 0
                while times < 120:
                    if os.path.exists(_download_file):
                        break
                    time.sleep(5)
                    times += 1
        pass

    def put_object_with_uri(self, uri, data, metadata=None):
        self.fds_client.put_object_with_uri(uri, data, metadata)

    def post_object(self, bucket_name, data, metadata=None):
        self.fds_client.post_object(bucket_name, data, metadata)

    def put_object(self, bucket_name, object_name, data, metadata=None):
        self.fds_client.put_object(bucket_name, object_name, data, metadata)
