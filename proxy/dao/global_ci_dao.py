# coding:utf-8

import time
import device_info as devinfo
import atexit

try:
    import pymongo
except ImportError:
    import global_ci_util.dependencies_util as dependencies_util
    dependencies_util.check_and_install_package('pymongo')
    import pymongo

from daoparam import *


class GlobalCiDao:

    __instance = None

    def __init__(self):
        print('Global CI Database access object init')
        self.mongo_client = pymongo.MongoClient(host="10.56.43.25")
        self.db = self.mongo_client[DATABASE_GLOBAL_CI]
        atexit.register(self.release)

    def release(self):
        print('Release mongo client')
        self.mongo_client.close()

    @staticmethod
    def get_single_instance():
        if GlobalCiDao.__instance is None:
            GlobalCiDao.__instance = GlobalCiDao()
        return GlobalCiDao.__instance

    def get_collection_issue_records(self):
        return self.db[COLLECTION_ISSUE_RECORDS]

    def get_collection_omni_test_records(self):
        return self.db[COLLECTION_OMNI_TEST_RECORDS]

    def save_test_begin(self, serial, omni_task_id, omni_exec_id, tester, script_type, pkg_name, apk_build_id):
        coll = self.db[COLLECTION_OMNI_TEST_RECORDS]

        data = {FIELD_TESTER: tester, FIELD_SCRIPT_TYPE: script_type, FIELD_PACKAGE_NAME: pkg_name,
                FIELD_OMNI_TASK_ID: omni_task_id, FIELD_OMNI_EXEC_ID: omni_exec_id, FIELD_APK_BUILD_ID:apk_build_id}

        # device_module, android_version
        data[FIELD_PRODUCT] = devinfo.get_device_name(serial)
        data[FIELD_DEVICE_MOD] = devinfo.get_mod_device_name(serial)
        data[FIELD_ROM_VERSION] = devinfo.get_rom_version(serial)
        data[FIELD_ANDROID_VERSION] = devinfo.get_android_version(serial)
        data[FIELD_BUILD_TAGS] = devinfo.get_device_rom_signature(serial)

        data[FIELD_BEGIN_TIME] = int(time.time() * 1000)

        return coll.insert(data)

    def save_test_finish(self, record_id, test_result, error_reason=None, **kwargs):
        coll = self.db[COLLECTION_OMNI_TEST_RECORDS]

        current_time = time.time() * 1000
        query = {FIELD_ID: record_id}
        begin_time = coll.find_one(query)[FIELD_BEGIN_TIME]

        data = {"$set": {FIELD_END_TIME: int(current_time),
                         FIELD_DURATION: int((current_time-begin_time)/1000),
                         FIELD_TEST_RESULT: test_result
                         }
                }
        if error_reason is not None:
            data['$set'][FIELD_ERROR_REASON] = error_reason

        if kwargs is not None:
            for k, v in kwargs.items():
                data['$set'][k] = v
        print(data)
        coll.update_one(query, data)
        pass

    def add_issue_record(self, jira_id, script_type, package_name, tester, happen_count, jira_status_change,
                         apk_build_id, issue_time=int(time.time() * 1000), **kwargs):
        data = {
            FIELD_JIRA_ID: jira_id,
            FIELD_APK_BUILD_ID: apk_build_id,
            FIELD_SCRIPT_TYPE: script_type,
            FIELD_PACKAGE_NAME: package_name,
            FIELD_TESTER: tester,
            FIELD_HAPPEN_COUNT: happen_count,
            FIELD_ISSUE_TIME: issue_time,
            FIELD_JIRA_STATUS_CHANGE: jira_status_change
        }
        if kwargs is not None:
            for k, v in kwargs.items():
                data[k] = v

        coll = self.db[COLLECTION_ISSUE_RECORDS]
        coll.insert(data)

    def get_collection(self, collection_name):
        return self.db[collection_name]
