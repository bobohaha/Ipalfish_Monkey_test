# -*- encoding: utf-8 -*-
import datetime
import sys

import param
from monkeyTest.MonkeyApkTester import MonkeyApkTester
from .preSetting import PreSetter
from monkeyTest.BugDao import BugDao
from monkeyTest.MonkeyJiraParam import USERNAME
from .preSetting import TestRegionLanguageBuilder
from global_ci_util import LogUtil
from monkeyReportGenerating.MonkeyReportGenerator import MonkeyReportGenerator
from .config.account import *
import version as version
from global_ci_util.ci_quality.api_param import *

reload(sys)
sys.setdefaultencoding('utf-8')


class proxy:
    _run = None
    _rst = False
    _jira_keys = list()

    def __init__(self, run):
        LogUtil.log_start("__init__")
        LogUtil.log("Current code version: " + version.__version__)
        self.mongo_record_id_of_test_info = None
        self._run = run
        self._MonkeyApkTester = None
        self._PreSetter = None

        self._preset_target_region_language = TestRegionLanguageBuilder.get_target_region_language(run._param_dict[param.TARGET_LANGUAGE],
                                                                                                   run._param_dict[param.TARGET_REGION]) \
            if param.TARGET_LANGUAGE in run._param_dict.keys() \
            else dict()

        self.tag = run._param_dict[param.PACKAGE_NAME] + "_" + str(datetime.datetime.now())
        self.is_auto_test = run._param_dict[param.CI_TEST_RECORD_ID] != "None"
        self.tester = USERNAME if self.is_auto_test else run._param_dict[param.TESTER]
        self._rst_fail_msg = None
        self._test_information = None
        self._kernel_issues = None
        self._not_submitted_issues = None
        LogUtil.log_end("__init__")

    def do_script(self):
        LogUtil.log_start("doScript")
        self.test_start()

        self.download_test_apk()
        if self.get_result() is False:
            self._rst_fail_msg = "下载待测Apk失败<BR>" \
                                 "Download test apk error"
            self.test_end(TEST_STATUS_EXCEPTION)
            return

        self.install_test_apk()
        if self.get_result() is False:
            self._rst_fail_msg = "安装待测Apk失败<BR>" \
                                 "Install test apk error"
            self.test_end(TEST_STATUS_EXCEPTION)
            return

        self.check_package_valid()
        if not self._rst:
            self._rst_fail_msg = "指定包名不可用<BR>" \
                                 "Specified package name invalid"
            self.test_end(TEST_STATUS_EXCEPTION)
            return

        self.granting_package_permission()
        self.pre_setting()
        if self.get_result() is False:
            self._rst_fail_msg = "设置预置条件失败<BR>" \
                                 "Presetting error"
            self.test_end(TEST_STATUS_EXCEPTION)
            return

        self.run_monkey_test()

        self.remove_accounts()
        test_status = TEST_STATUS_PASSED if self._rst else TEST_STATUS_FAILED
        self.test_end(test_status)
        LogUtil.log_end("doScript")

    def pre_setting(self):
        LogUtil.log_start("Presetting for Monkey Test")
        self.init_pre_setter(target_region_language=self._preset_target_region_language)
        self._PreSetter.download_or_upgrade_apk()
        self._PreSetter.install_downloaded_apk()
        self._rst = self._PreSetter.get_result()
        if self._rst is False:
            LogUtil.log_end("Presetting for Monkey Test: Failed: install presetting apk error!")
            return

        self._PreSetter.run_presetting_ui()
        self._rst = self._PreSetter.get_result()
        if self._rst is False:
            LogUtil.log_end("Presetting for Monkey Test: Failed: PreSetting error!")
            return
        self._PreSetter.clear_pkg_cache_in_device()
        self._PreSetter.run_specific_set()
        LogUtil.log_end("Presetting for Monkey Test")

    def download_test_apk(self):
        LogUtil.log_start("download_test_apk")
        self.init_monkey_tester()
        self._MonkeyApkTester.download_test_apk()
        self._rst, self._jira_keys, self._kernel_issues, self._not_submitted_issues = self._MonkeyApkTester.get_rst()
        LogUtil.log_start("download_test_apk")

    def install_test_apk(self):
        LogUtil.log_start("install_test_apk")
        self.init_monkey_tester()
        self._MonkeyApkTester.check_and_sign_apk()
        self._MonkeyApkTester.install_downloaded_test_apk()
        self._rst, self._jira_keys, self._kernel_issues, self._not_submitted_issues = self._MonkeyApkTester.get_rst()
        LogUtil.log_end("install_test_apk: " + str(self._rst))

    def check_package_valid(self):
        LogUtil.log_start("check_package_valid")
        self.init_monkey_tester()
        self._rst = self._MonkeyApkTester.check_package_valid()
        LogUtil.log_end("check_package_valid")

    def granting_package_permission(self):
        LogUtil.log_start("granting_package_permission")
        self.init_monkey_tester()
        self._MonkeyApkTester.grant_permissions()
        LogUtil.log_end("granting_package_permission")

    def run_monkey_test(self):
        LogUtil.log_start("Monkey Test")
        self.init_monkey_tester()
        self._MonkeyApkTester.run_test()
        self._rst, self._jira_keys, self._kernel_issues, self._not_submitted_issues = self._MonkeyApkTester.get_rst()
        if self._rst is False:
            self._rst_fail_msg = "Monkey test failed"
        LogUtil.log("Monkey Test Result: " + str(self._rst))
        LogUtil.log_end("Monkey Test")

    def remove_accounts(self):
        LogUtil.log_start("remove_accounts")
        self.init_pre_setter()
        self._PreSetter.remove_accounts()
        LogUtil.log_end("remove_accounts")
        pass

    def get_result(self):
        return self._rst

    def generate_test_report(self):
        MonkeyReportGenerator(self._run._serial,
                              self._run._out_path,
                              self._run._param_dict,
                              self._rst,
                              self._rst_fail_msg,
                              self._jira_keys,
                              self._kernel_issues,
                              self._not_submitted_issues).generate_result_report()
        pass

    def record_test_info(self):
        self.init_monkey_tester()
        for _ in range(0, 3):
            self.mongo_record_id_of_test_info = self._MonkeyApkTester.record_test_info_to_mongo()
            if self.mongo_record_id_of_test_info is not None:
                return

    def record_test_done(self):
        for _ in range(0, 3):
            if BugDao.add_test_done_to_use_info_record(self.tag):
                BugDao.add_test_finish_record_to_mongo(record_id=self.mongo_record_id_of_test_info,
                                                       test_result=self._rst,
                                                       error_reason=self._rst_fail_msg)
                return True

    def init_monkey_tester(self):
        if self._MonkeyApkTester is None:
            LogUtil.log(">> =======Init monkey tester========")
            self._MonkeyApkTester = MonkeyApkTester(self._run._serial,
                                                    self._run._out_path,
                                                    self._run._param_dict,
                                                    self.tag)
            LogUtil.log(">> =======Init monkey tester done========")

    def init_pre_setter(self, target_region_language=None):
        if self._PreSetter is None:
            LogUtil.log(">> =======Init pre-setter========")
            if target_region_language is None:
                target_region_language = list()
            self._PreSetter = PreSetter(self._run._serial,
                                        self._run._out_path,
                                        self._run._param_dict[param.PACKAGE_NAME],
                                        target_region_language,
                                        fds_access_key,
                                        fds_access_secret)
            LogUtil.log(">> =======Init pre-setter done========")

    def test_start(self):
        self.init_monkey_tester()
        self._MonkeyApkTester.test_start()

    def test_end(self, test_status):
        self.init_monkey_tester()
        self._MonkeyApkTester.test_end(test_status=test_status)
