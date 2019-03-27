# -*- encoding: utf-8 -*-
import datetime
import sys

import param
from monkeyTest.MonkeyApkTester import MonkeyApkTester
from preSetting.PreSetter import PreSetter
from recoverDevice.DeviceRecover import DeviceRecover
from skipOOBE.SkipOOBE import SkipOOBE
from utils.DependenciesUtil import DependenciesUtil
from utils.LogUtil import LogUtil
from monkeyReportGenerating.MonkeyReportGenerator import MonkeyReportGenerator

reload(sys)
sys.setdefaultencoding('utf-8')


class proxy:
    _run = None
    _rst = False
    _jira_keys = list()

    def __init__(self, run):
        LogUtil.log_start("__init__")
        DependenciesUtil.install_dependencies()
        self._run = run
        self._MonkeyApkTester = None
        self._PreSetter = None

        self.tag = run._param_dict['PACKAGE_NAME'] + "_" + str(datetime.datetime.now())
        self._rst_fail_msg = None
        self._test_information = None
        self._kernel_issues = None
        self._not_submitted_issues = None

    def do_script(self):
        LogUtil.log_start("doScript")
        # self.recover_device()
        # if self.get_result() is False:
        #     return
        #
        # self.skip_oobe()
        # if self.get_result() is False:
        #     return

        self.install_test_apk()
        if self.get_result() is False:
            self._rst_fail_msg = "安装待测Apk失败"
            return

        self.check_package_valid()
        if not self._rst:
            self._rst_fail_msg = "指定包名不可用"
            return

        self.pre_setting()
        if self.get_result() is False:
            self._rst_fail_msg = "设置预置条件失败"
            return

        self.run_monkey_test()

        self.remove_accounts()
        LogUtil.log_end("doScript")

    def recover_device(self):
        LogUtil.log_start("Recovery Devices for Monkey Test")
        _DeviceRecover = DeviceRecover(self._run._serial)
        _DeviceRecover.recover_device()
        self._rst = _DeviceRecover.get_result()
        LogUtil.log_end("Recovery Devices for Monkey Test: " + str(self._rst))

    def skip_oobe(self):
        LogUtil.log_start("Skip OOBE for Monkey Test")
        test_region_language = {}
        _SkipOOBE = SkipOOBE(self._run._serial,
                             self._run._out_path,
                             self._run._param_dict,
                             test_region_language)
        _SkipOOBE.download_or_upgrade_apk()
        _SkipOOBE.make_sure_in_oobe()
        _SkipOOBE.install_downloaded_apk()
        self._rst = _SkipOOBE.get_result()
        if self._rst is False:
            LogUtil.log_end("Skip OOBE for Monkey Test: Failed: install skipOOBE.apk error")
            return

        _SkipOOBE.run_skip_oobe()
        self._rst = _SkipOOBE.get_result()
        if self._rst is False:
            LogUtil.log_end("Skip OOBE for Monkey Test: Failed: _SkipOOBE fail")
            return
        _SkipOOBE.clear_pkg_cache_in_device()
        LogUtil.log_end("Skip OOBE for Monkey Test")

    def pre_setting(self):
        LogUtil.log_start("Presetting for Monkey Test")
        if self._PreSetter is None:
            self._PreSetter = PreSetter(self._run._serial,
                                        self._run._out_path,
                                        self._run._param_dict[param.PACKAGE_NAME])
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

    def install_test_apk(self):
        LogUtil.log_start("install_test_apk")
        if self._MonkeyApkTester is None:
            self._MonkeyApkTester = MonkeyApkTester(self._run._serial,
                                                    self._run._out_path,
                                                    self._run._param_dict,
                                                    self.tag)
        self._MonkeyApkTester.download_test_apk()
        self._MonkeyApkTester.check_and_sign_apk()
        self._MonkeyApkTester.install_downloaded_test_apk()
        self._rst, self._jira_keys, self._kernel_issues, self._not_submitted_issues = self._MonkeyApkTester.get_rst()
        LogUtil.log_end("install_test_apk: " + str(self._rst))

    def check_package_valid(self):
        LogUtil.log_start("check_package_valid")
        if self._MonkeyApkTester is None:
            self._MonkeyApkTester = MonkeyApkTester(self._run._serial,
                                                    self._run._out_path,
                                                    self._run._param_dict,
                                                    self.tag)
        self._rst = self._MonkeyApkTester.check_package_valid()
        LogUtil.log_end("check_package_valid")

    def run_monkey_test(self):
        LogUtil.log_start("Monkey Test")
        if self._MonkeyApkTester is None:
            self._MonkeyApkTester = MonkeyApkTester(self._run._serial,
                                                    self._run._out_path,
                                                    self._run._param_dict,
                                                    self.tag)
        self._MonkeyApkTester.run_test()
        self._rst, self._jira_keys, self._kernel_issues, self._not_submitted_issues = self._MonkeyApkTester.get_rst()
        LogUtil.log("Monkey Test Result: " + str(self._rst))
        LogUtil.log_end("Monkey Test")

    def remove_accounts(self):
        LogUtil.log_start("remove_accounts")
        if self._PreSetter is None:
            self._PreSetter = PreSetter(self._run._serial,
                                        self._run._out_path,
                                        self._run._param_dict[param.PACKAGE_NAME])
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
