DEBUG = True
DATABASE_GLOBAL_CI = 'global_ci' if not DEBUG else 'global_ci_dev'
COLLECTION_OMNI_TEST_RECORDS = 'omni_test_records'
COLLECTION_ISSUE_RECORDS = 'issue_records'

# Fields for COLLECTION_OMNI_TEST_RECORDS
FIELD_ID = '_id'
FIELD_APK_BUILD_ID = 'apk_build_id'
FIELD_TESTER = 'tester'
FIELD_SCRIPT_TYPE = 'script_type'
FIELD_PACKAGE_NAME = 'package_name'
FIELD_OMNI_TASK_ID = 'omni_task_id'
FIELD_OMNI_EXEC_ID = 'omni_exec_id'
FIELD_BEGIN_TIME = 'begin_time'
FIELD_END_TIME = 'finish_time'
FIELD_DURATION = 'duration'
FIELD_TEST_RESULT = 'test_result' # One of VALUE_TEST_RESULT_SUCCESS, VALUE_TEST_RESULT_FAILED, VALUE_TEST_RESULT_CANCELED
FIELD_ERROR_REASON = 'error_reason'

# Device information
FIELD_PRODUCT = 'product'
FIELD_DEVICE_MOD = 'device_module'
FIELD_ANDROID_VERSION = 'android_version'
FIELD_ROM_VERSION = 'rom_version'
FIELD_BUILD_TAGS = 'build_tags'

# Fields for COLLECTION_ISSUE_RECORDS
FIELD_JIRA_ID = 'jira_id'
FIELD_JIRA_LABELS = 'jira_labels'
FIELD_JIRA_SUMMARY = 'jira_summary'
FIELD_JIRA_BUG_CATEGORY = 'jira_bug_category'
FIELD_JIRA_ASSIGNEE = 'jira_assigee'
FIELD_BUG_SUMMARY = 'bug_summary'
FIELD_HAPPEN_COUNT = 'happen_count'
FIELD_ISSUE_TIME = 'issue_time'
FIELD_JIRA_STATUS_CHANGE = 'jira_status_change'

# Value of FIELD_TEST_RESULT
VALUE_TEST_RESULT_SUCCESS = 'success'
VALUE_TEST_RESULT_FAILED = 'failed'
VALUE_TEST_RESULT_CANCELED = 'canceled'

# Value of FIELD_JIRA_STATUS_CHANGE
VALUE_JIRA_STATUS_CHANGE_REOPEN = 'reopen'
VALUE_JIRA_STATUS_CHANGE_ALREADY_EXIST = 'already exist'
VALUE_JIRA_STATUS_CHANGE_NEW = 'new'
VALUE_JIRA_STATUS_CHANGE_NOT_REOPEN = 'not reopen'
