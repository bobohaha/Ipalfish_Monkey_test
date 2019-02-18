from proxy.utils.PropUtil import PropUtil
from proxy.utils.ADBUtil import ADBUtil
from proxy.monkeyTest.BugDao import BugDao
from proxy.utils.ehp_pyhon2 import *
from proxy.utils.JIRAParam import JIRA_ISSUE_LINK
from proxy.utils.PathUtil import PathUtil
from proxy.utils.LogUtil import LogUtil

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class MonkeyReportGenerator(object):
    def __init__(self, serial, out_path, param_dict, rst, rst_fail_msg, jira_keys):
        self.test_result = self.TestResult(rst, rst_fail_msg)
        self.test_information = self.TestInformation(serial, param_dict)
        self.issue_detail = self.IssueDetails(jira_keys)

        self.html = Html()
        self.report_content = self.html.fromfile(PathUtil.get_file_path(__file__) + "/MonkeyReportTemplate.html")
        self.result_file_path = out_path + "/result.html"
        pass

    def process_test_result(self):
        LogUtil.log_start("process_test_result")
        test_result_item = self.report_content.byid('test-result')
        test_result_str = "Passed" if self.test_result.rst else "Failed"
        test_result_item.attr['style'] = "background: white; color: green" \
            if self.test_result.rst else "background: white; color: red"
        test_result_item.append(Data(test_result_str))
        if self.test_result.fail_msg is None or self.test_result.fail_msg is "None":
            LogUtil.log("no fail reason .....")
            root, fail_reason_item = self.report_content.fst_with_root('tr', ('id', 'fail-reason'))
            root.remove(fail_reason_item)
        else:
            fail_reason_msg_item = self.report_content.byid('fail-reason-msg')
            fail_reason_msg_item.append(Data(self.test_result.fail_msg))
        LogUtil.log_end("process_test_result")
        pass

    def process_test_information(self):
        LogUtil.log_start("process_test_information")
        test_package_item = self.report_content.byid('test-package')
        test_package_item.append(Data(self.test_information.package_name))

        test_apk_version_item = self.report_content.byid('apk-version')
        test_apk_version_item.append(Data(self.test_information.app_versions))

        if self.test_information.jenkins_build_num is None or self.test_information.jenkins_build_num == "None":
            LogUtil.log("Not auto test....")
            root, jenkins_build_num_str = self.report_content.fst_with_root('tr', ('id', 'apk-build-version'))
            root.remove(jenkins_build_num_str)
        else:
            jenkins_build_num_item = self.report_content.byid('apk-build-version-msg')
            jenkins_build_num_item.append(Data(self.test_information.jenkins_build_num))

        test_device_item = self.report_content.byid('test-device')
        test_device_item.append(Data(self.test_information.device_name))

        test_device_version_item = self.report_content.byid('device-version')
        test_device_version_item.append(Data(self.test_information.rom_version))

        test_android_version_item = self.report_content.byid('android-version')
        test_android_version_item.append(Data(self.test_information.android_version))

        test_monkey_param_item = self.report_content.byid('monkey-param')
        test_monkey_param_item.append(Data(self.test_information.monkey_param))

        test_monkey_time_item = self.report_content.byid('monkey-time')
        test_monkey_time_item.append(Data(self.test_information.monkey_time))
        LogUtil.log_end("process_test_information")
        pass

    def process_issue_details(self):
        LogUtil.log_start("process_issue_details")
        issue_count = len(self.issue_detail.jiras) if self.issue_detail.jiras is not None else 0
        if self.issue_detail.jiras is None or issue_count == 0:
            LogUtil.log("There is no issue...")
            root, issue_section = self.report_content.fst_with_root('section', ('class', 'IssueDetailsCard'))
            root.remove(issue_section)
        else:
            self.set_issue_detail_tags(issue_count)
            self.set_issue_detail_contents()
        LogUtil.log_end("process_issue_details")
        pass

    def set_issue_detail_contents(self):
        LogUtil.log_start("set_issue_detail_contents")
        issue_detail_items = self.report_content.find('tr', ('class', 'issue-detail'))
        ind = 0
        print type(issue_detail_items)
        for issue_detail_item in issue_detail_items:
            try:
                issue_items = issue_detail_item.find('td')
                index = 1
                for issue_item in issue_items:
                    issue_info = self.issue_detail.jiras[0].get() if self.issue_detail.jiras[0] is not None else None
                    index = self.set_issue_info(index, issue_item, ind+1, issue_info)

                self.issue_detail.jiras = self.issue_detail.jiras[1:]
                ind += 1
            except (ValueError, KeyError):
                LogUtil.log("set issue detail error")
        LogUtil.log_end("set_issue_detail_contents")
        pass

    def set_issue_info(self, index, issue_item, issue_no, issue_jira):
        if issue_item.text() == "" and index == 1:
            issue_item.append(Data(str(issue_no)))

        if issue_item.text() == "" and index == 2:
            jira_id = issue_jira.jira_id if issue_jira is not None else "error jira key"
            issue_item.insert(0, self.JiraKey(jira_id))

        if issue_item.text() == "" and index == 3:
            jira_summary = issue_jira.jira_summary if issue_jira is not None else "error jira summary"
            issue_item.append(Data(jira_summary))

        return index+1

    def set_issue_detail_tags(self, issue_count):
        LogUtil.log_start("set_issue_detail_tags")
        issue_detail_count = self.get_issue_tag_count()
        ind = 0
        while ind < issue_count - issue_detail_count:
            root, issue_detail_item = self.report_content.fst_with_root('tr', ('class', 'issue-detail'))
            issue_detail_target = self.html.feed(str(issue_detail_item))
            root.insert_after(issue_detail_item, issue_detail_target)
            ind += 1
        LogUtil.log_end("set_issue_detail_tags")

    def get_issue_tag_count(self):
        count = 0
        issue_detail_items = self.report_content.find('tr', ('class', 'issue-detail'))
        for _ in issue_detail_items:
            count += 1
        return count

    def generate_result_report(self):
        LogUtil.log_start("generate_result_report")
        self.process_test_result()
        self.process_test_information()
        self.process_issue_details()
        self.report_content.write(self.result_file_path)
        LogUtil.log_end("generate_result_report")
        pass

    class JiraKey(Tag):
        def __init__(self, jira_key):
            href = JIRA_ISSUE_LINK.format(issueIdOrKey=jira_key)
            self.attr = {'href': href}
            Tag.__init__(self, 'a', attr=self.attr)
            self.append(Data(jira_key))
            pass

    class TestResult:
        def __init__(self, rst, fail_msg):
            self.rst = rst
            self.fail_msg = fail_msg
            pass

    class TestInformation:
        def __init__(self, serial, param_dict):
            self.package_name = param_dict['PACKAGE_NAME']
            self.app_versions = str(MonkeyReportGenerator.AppVersions(serial, self.package_name.split(',')))
            self.jenkins_build_num = param_dict['TEST_APK_BUILD_VERSION']
            self.device_name = PropUtil.get_device_name(serial)
            self.rom_version = PropUtil.get_rom_version(serial)
            self.android_version = PropUtil.get_android_version(serial)
            self.monkey_param = param_dict['MONKEY_PARAM']
            self.monkey_time = "{loop} loop {minutes} {min_str}". \
                format(loop=param_dict['MONKEY_ROUND'],
                       minutes=param_dict['MONKEY_ROUND_MAXIMUM_TIME'],
                       min_str="minute" if param_dict['MONKEY_ROUND_MAXIMUM_TIME'] == 1 else "minutes")

    class AppVersions:
        def __init__(self, serial, package_names):
            self.app_version = dict()
            for package in package_names:
                _version = ADBUtil.get_installed_package_version(serial, package)
                self.app_version[package] = _version if _version else "Not installed"
                pass

        def __str__(self):
            app_versions_str = ""
            print self.app_version
            for k, v in self.app_version.iteritems():
                app_versions_str += k + ": " + v + "\n"

            app_versions_str.strip("\n")
            return app_versions_str

    class IssueDetails:
        def __init__(self, jira_keys):
            self.jiras = list()
            for jira_key in jira_keys:
                self.jiras.append(BugDao.get_jiras_by_jira_key(jira_key))
            pass
