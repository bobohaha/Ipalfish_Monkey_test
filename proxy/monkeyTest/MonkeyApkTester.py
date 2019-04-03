# coding=utf-8
import datetime
import re
import sys
from time import sleep, time

from proxy.param import MONKEY_SEED, PACKAGE_NAME, MONKEY_ROUND, MONKEY_PARAM, MONKEY_ROUND_MAXIMUM_TIME, ISSUE_WATCHERS, TESTER
from proxy.utils.ShellUtil import ShellUtil

reload(sys)
sys.setdefaultencoding('utf-8')

import zipfile
try:
    import zlib
    compression = zipfile.ZIP_DEFLATED
except ImportError:
    compression = zipfile.ZIP_STORED

from proxy.utils.BasUtil import BasUtil
from BugDao import BugDao
from BugModel import *
from MonkeyJiraTemplates import *
from MonkeyJiraUtil import *
from proxy.monkeyReportGenerating.MonkeyReportGenerator import MonkeyReportGenerator

try:
    import xlsxwriter
except ImportError:
    os.system("pip install XlsxWriter")
    import xlsxwriter

from proxy import param
from proxy.monkeyTest.MonkeyApkSyncUtil import MonkeyApkSyncUtil
from proxy.utils.ADBUtil import ADBUtil
from proxy.utils.KillProcessUtil import KillProcessUtil
from proxy.utils.LogUtil import LogUtil
from proxy.utils.PathUtil import PathUtil
from proxy.utils.PropUtil import PropUtil
from proxy.utils.sign_apk.SignAPKUtil import SignAPKUtil


SLEEP_TIME_2MIN = 60 * 2


class MonkeyApkTester:
    CURRENT_PATH = PathUtil.get_file_path(__file__)

    OUTPUT_PATH = "{out_put}/monkey_log/"
    RESULT_PATH = OUTPUT_PATH + "/result.xlsx"
    OUTPUT_CRASH_PATH = OUTPUT_PATH + "crash/"
    OUTPUT_ANR_PATH = OUTPUT_PATH + "anr/"

    DEVICE_OUTPUT_PATH = "/sdcard/monkeyApkTester_monkey_log/"
    DEVICE_OUTPUT_CRASH_PATH = DEVICE_OUTPUT_PATH + "crash/"
    DEVICE_OUTPUT_ANR_PATH = DEVICE_OUTPUT_PATH + "anr/"

    BUG_TYPE_CRASH = "app_crash"
    BUG_TYPE_ANR = "anr_"

    test_apk_file_name = ""
    test_apk_package = ""

    _log_file_name_origin = "monkey_log_{}.txt"
    _log_file_name = ""
    _monkey_command = ""

    results = {}
    results_monkey_time = dict()
    current_index = 0
    result_monkey_start_time_field = "monkey_start_time"
    result_monkey_issue_fst_time = "monkey_fst_time"
    result_monkey_issue_times = "monkey_issue_times"
    result_monkey_issue_summary = "monkey_issue_summary"
    bugs = {}

    MONKEY_CHECK_INTERVAL_SECOND = 60

    _MonkeyApkSyncUtil = None

    _rst = None
    _kernel_issues = None
    _not_submitted_issues = None

    def __init__(self, serial, out_path, param_dict, tag):
        self._device_serial = serial
        self._log_out_path = out_path
        self._param_dict = param_dict
        self._is_auto_test = True if self._param_dict[param.TEST_APK_BUILD_VERSION] != "None" else False
        self._seed = None
        self._seed_specify = param_dict[MONKEY_SEED] if MONKEY_SEED in param_dict.keys() \
                                                          and param_dict[MONKEY_SEED] is not None \
                                                          and param_dict[MONKEY_SEED] != "None" \
                                                          and param_dict[MONKEY_SEED] != "" \
                                                          and param_dict[MONKEY_SEED] != " " else None
        self.clear_log_folder()
        self._device_name = PropUtil.get_mod_device_name(serial)
        self._rom_version = PropUtil.get_rom_version(serial)
        self._MonkeyApkSyncUtil = MonkeyApkSyncUtil(self._param_dict[param.PACKAGE_NAME])
        self.tag = tag
        self.jira_keys = list()
        self.bug_seed = dict()

        self.OUTPUT_PATH = self.OUTPUT_PATH.format(out_put=self._log_out_path)
        self.RESULT_PATH = self.RESULT_PATH.format(out_put=self._log_out_path)
        self.OUTPUT_CRASH_PATH = self.OUTPUT_CRASH_PATH.format(out_put=self._log_out_path)
        self.OUTPUT_ANR_PATH = self.OUTPUT_ANR_PATH.format(out_put=self._log_out_path)
        pass

    def download_test_apk(self):
        if not self._is_auto_test:
            return
        LogUtil.log_start("download_test_apk")
        _PathUtil = PathUtil(__file__)
        _PathUtil.chdir_here()
        self._MonkeyApkSyncUtil. \
            download_objects_with_version(self._param_dict[param.TEST_APK_BUILD_VERSION])
        self.test_apk_file_name = self.get_file_name(".apk")
        self.test_apk_package = ShellUtil.get_apk_package_name(self.test_apk_file_name)
        LogUtil.log_end("download_test_apk")

    def uninstall_apk_in_device(self):
        if not self._is_auto_test:
            return
        LogUtil.log_start("uninstall_apk_in_device")
        self._rst = ADBUtil.try_uninstall(self._device_serial, self.test_apk_package)
        LogUtil.log_end("uninstall_apk_in_device")
        pass

    def check_and_sign_apk(self):
        if not self._is_auto_test:
            return
        LogUtil.log_start("retry_sign_apk")
        if ADBUtil.check_package_exist(self._device_serial, self.test_apk_package) and not self.is_apk_in_device_belong_normal_key():
            self.test_apk_file_name = SignAPKUtil.get_test_key_apk_if_belong_normal_key(self.test_apk_file_name)
        LogUtil.log_end("retry_sign_apk")

    def install_downloaded_test_apk(self):
        if not self._is_auto_test:
            return
        LogUtil.log_start("install_downloaded_test_apk")
        self._rst = ADBUtil.try_install(self._device_serial, self.test_apk_file_name)
        LogUtil.log_end("install_downloaded_test_apk")

    def reboot_device(self):
        ADBUtil.reboot(self._device_serial)
        pass

    def clear_log_folder(self):
        if os.path.exists(self.OUTPUT_PATH):
            command = "rm -rf " + self.OUTPUT_PATH
            print command
            os.system(command)

        ADBUtil.rm(self._device_serial, self.DEVICE_OUTPUT_PATH)

        if os.path.exists(self._log_out_path):
            command = "rm -rf " + self._log_out_path
            print command
            os.system(command)

        command = "mkdir -p " + self._log_out_path
        print command
        os.system(command)

    def check_package_valid(self):
        package_list = self._param_dict[PACKAGE_NAME].split(",")
        for package in package_list:
            if package.rstrip() == "":
                continue
            package_valid = ADBUtil.check_package_exist(self._device_serial, package)
            if not package_valid:
                return False
        return True
        pass

    def run_test(self):
        LogUtil.log_start("run_test")
        self._rst = True
        round_str = self._param_dict[MONKEY_ROUND]

        round_count = int(round_str)

        for round_index in range(1, round_count + 1):
            self.current_index = round_index
            self.test(round_index)

        self.copy_files_to_output_path()
        self.create_jira_or_add_comment()
        LogUtil.log_end("run_test")

    def test(self, round_index):
        LogUtil.log_start("test: " + str(round_index))
        self.reboot_device()
        self.clear_device_log()
        ADBUtil.silence_and_disable_notification_in_device(self._device_serial)

        self.results_monkey_time[self.current_index] = dict()
        self.results_monkey_time[self.current_index][self.result_monkey_start_time_field] = ADBUtil.get_date_time(self._device_serial)
        self.run_monkey_in_background()
        running_time = self.hold_for_monkey_run_time()
        self.kill_monkey()

        self.pull_log(round_index)
        self.analyze_log(round_index, running_time)
        self.reboot_device()
        LogUtil.log_end("test: " + str(round_index))

    def kill_monkey(self):

        LogUtil.log_start("kill_monkey")

        KillProcessUtil.kill_device_process(self._device_serial, "monkey")

        LogUtil.log_end("kill_monkey")

    def init_monkey_command(self):
        LogUtil.log_start("init_monkey_command")
        input_package_name = self._param_dict[PACKAGE_NAME]
        monkey_param = self._param_dict[MONKEY_PARAM]

        package_name_ary = input_package_name.split(",")
        package_name_str = ""

        for package_name in package_name_ary:
            package_name_str = package_name_str + "-p " + package_name + " "

        self._log_file_name = self._log_file_name_origin.format(str(self.current_index))
        log_file_full_path = self._log_out_path + "/" + self._log_file_name

        command = "monkey " \
                  + monkey_param + " " + package_name_str

        self.get_seed()
        if self._seed is not None:
            command = command + "-s " + self._seed + " "

        command = command + "50000000 > " + log_file_full_path + " & "
        self._monkey_command = command
        LogUtil.log("monkey command: " + self._monkey_command)
        LogUtil.log_end("init_monkey_command")

    def run_monkey_in_background(self):
        LogUtil.log_start("run_monkey_in_background")

        self.init_monkey_command()
        ADBUtil.execute_shell(self._device_serial, self._monkey_command)

        LogUtil.log_end("run_monkey_in_background")

    def hold_for_monkey_run_time(self):
        LogUtil.log_start("hold_for_monkey_run_time")

        start_time = time()
        monkey_round_maximum_time_min = self._param_dict[MONKEY_ROUND_MAXIMUM_TIME]
        monkey_max_time = int(monkey_round_maximum_time_min) * 60

        LogUtil.log("hold_for_monkey_run_time(): monkey_round_maximum_time_min is " + monkey_round_maximum_time_min)

        while True:
            left_seconds = start_time + monkey_max_time - time()
            if left_seconds <= 0:
                break
            LogUtil.log("hold_for_monkey_run_time(): left {} minutes...".format(str(left_seconds / 60)))
            sleep(self.MONKEY_CHECK_INTERVAL_SECOND)
            if ADBUtil.get_process_id_by_name(self._device_serial, "monkey") is None:
                self.run_monkey_in_background()

        end_time = time()

        LogUtil.log_end("hold_for_monkey_run_time")

        return end_time - start_time

    def pull_log(self, round_index):

        ADBUtil.mkdir_p(self._device_serial, self.DEVICE_OUTPUT_CRASH_PATH + "round_" + str(round_index) + "/")
        ADBUtil.move(self._device_serial, "/sdcard/app_crash* ",
                     self.DEVICE_OUTPUT_CRASH_PATH + "round_" + str(round_index) + "/")
        ADBUtil.move(self._device_serial, "/data/app_crash/traces* ",
                     self.DEVICE_OUTPUT_CRASH_PATH + "round_" + str(round_index) + "/")

        command = "mkdir -p " + self.OUTPUT_CRASH_PATH
        print command
        os.system(command)
        #
        ADBUtil.pull(self._device_serial,
                     self.DEVICE_OUTPUT_CRASH_PATH + "round_" + str(round_index) + "/",
                     self.OUTPUT_CRASH_PATH)

        ADBUtil.mkdir_p(self._device_serial,
                        self.DEVICE_OUTPUT_ANR_PATH + "round_" + str(round_index) + "/")
        ADBUtil.move(self._device_serial, "/sdcard/anr_* ",
                     self.DEVICE_OUTPUT_ANR_PATH + "round_" + str(round_index) + "/")
        ADBUtil.move(self._device_serial, "/data/anr/traces* ",
                     self.DEVICE_OUTPUT_ANR_PATH + "round_" + str(round_index) + "/")

        command = "mkdir -p " + self.OUTPUT_ANR_PATH
        print command
        os.system(command)
        #
        ADBUtil.pull(self._device_serial,
                     self.DEVICE_OUTPUT_ANR_PATH + "round_" + str(round_index) + "/",
                     self.OUTPUT_ANR_PATH)
        pass

    def analyze_log(self, round_index, running_time):
        self.get_seed()
        command = "ls " + self.OUTPUT_CRASH_PATH + "round_" + str(
            round_index) + "/app_crash*"
        output = os.popen(command)
        result = output.read().strip()

        crash_str = ""
        if not result + "x" == "x":
            file_list = result.split("\n")
            crash_str = self.analyze_bugs(file_list, self.BUG_TYPE_CRASH)
        else:
            pass

        command = "ls " + self.OUTPUT_ANR_PATH + "round_" + str(round_index) + "/anr_*"
        output = os.popen(command)
        result = output.read().strip()

        command_traces = "ls " + self.OUTPUT_ANR_PATH + "round_" + str(round_index) + "/traces*"
        output = os.popen(command_traces)
        result_traces = output.read().strip()

        traces_file_list = None
        if not result_traces + "x" == "x":
            traces_file_list = result_traces.split("\n")

        anr_str = ""
        if not result + "x" == "x":
            file_list = result.split("\n")
            anr_str = self.analyze_bugs(file_list, self.BUG_TYPE_ANR, trace_files=traces_file_list)
        else:
            pass

        running_min = running_time / 60
        running_sec = running_time % 60
        running_str = str(running_min) + " min + " + str(running_sec) + " sec."

        self.results[round_index] = {"seed": self._seed, "times": running_str,
                                     "crash": crash_str, "anr": anr_str}

    def get_seed(self):
        if self._seed_specify is not None:
            self._seed = self._seed_specify
            return

        log_file_full_path = self._log_out_path + "/" + self._log_file_name
        if self._log_file_name != "" and os.path.exists(log_file_full_path):
            log_file = open(log_file_full_path, 'r')
            for line in log_file:
                if ":Monkey:" in line:
                    self._seed = line.split("seed=")[1].split(" ")[0]
                    return
        else:
            self._seed = None

    def copy_files_to_output_path(self):
        LogUtil.log_start("move_result")
        command = "cp " + self.CURRENT_PATH + "/mapping.txt" + " " + self._log_out_path
        print command
        os.system(command)

        LogUtil.log_end("move_result")

    def analyze_bugs(self, bug_files, bug_type, trace_files=None):
        LogUtil.log_start("analyze_bugs")
        result = ""
        for filename in bug_files:
            if filename:
                bug = None
                if self.BUG_TYPE_CRASH == bug_type:
                    bug = self.get_crash_info(filename)
                elif self.BUG_TYPE_ANR == bug_type:
                    bug = self.get_anr_info(filename)
                    if trace_files is not None:
                        filename = [filename] + trace_files

                self.analysis_bug_bas(filename)
                if bug in self.bugs:
                    self.bugs[bug] = self.bugs[bug] + 1
                else:
                    self.bugs[bug] = 1
                result += bug + "\n"
        result = result.strip()
        return result

    def get_crash_info(self, filename):
        return self.BUG_TYPE_CRASH + re.findall(r"app_crash(.+?)_", filename)[0]

    def get_anr_info(self, filename):
        return self.BUG_TYPE_ANR + re.findall(r"anr_(.+?)_", filename)[0]

    def analysis_bug_bas(self, file_name):
        packages = self._param_dict[PACKAGE_NAME].split(",")
        if not isinstance(packages, list):
            packages = [packages]
        for package in packages:
            self.analyzing_and_saving(file_name, package)
        pass

    def analyzing_and_saving(self, file_name, package):
        bug_results = BasUtil().analysis(file_name, package)
        if isinstance(file_name, list):
            file_names = ""
            for name in file_name:
                file_names += name + ","
            file_name = file_names[:-1]
        if isinstance(bug_results, list) and len(bug_results) > 0:
            self._rst = False
            for bug_res in bug_results:
                save_result, bug = BugDao.save_bug_detail(bug_res, tag=self.tag)
                if save_result is False:
                    print("Save bug details error")
                    self.save_to_not_submitted_issues(bug_res['dgt'], bug_res['time'], bug_res['type'], bug_res['summary'], bug_res['pkgName'])
                    continue
                self.collect_bug_seed_info(bug.bug_signature_code)
                self.collect_bug_time_info(bug.bug_signature_code, bug.bug_time)
                print BugDao.save_bug_tag(bug.bug_signature_code, self.tag)
                print BugDao.save_bug_file(bug.bug_signature_code, file_name, self.tag)
                print BugDao.save_bug_rom(bug.bug_signature_code,
                                          self._device_name,
                                          get_miui_model(self._device_name),
                                          self._rom_version,
                                          self.tag)
        else:
            print "there is no bug about {} in {}".format(package, file_name)

    def get_rst(self):
        return self._rst, self.jira_keys, self._kernel_issues, self._not_submitted_issues

    def analyze_result(self):
        self._rst = len(self.bugs) == 0

    def clear_device_log(self):
        ADBUtil.rm(self._device_serial, self.DEVICE_OUTPUT_PATH)
        pass

    @classmethod
    def get_file_name(cls, keyword, file_path="./"):
        all_files = os.listdir(file_path)
        for f in all_files:
            if keyword in os.path.basename(f):
                return f
        return ""

    def create_jira_or_add_comment(self):
        LogUtil.log_start("create_jira_or_add_comment")
        bugs = self.get_bugs()
        if bugs is not None:
            LogUtil.log("Having bugs...")
            for bug in bugs:
                if bug.bug_package_name in (MintBrowser, Browser) and bug.bug_type == "ne" and bug.bug_summary.startswith("signal "):
                    LogUtil.log("Don't submit jira with kernel error on Browser or Mint Browser: " + bug.bug_summary)
                    self.save_to_kernel_issues(bug.bug_signature_code, bug.bug_summary, bug.bug_type, bug.bug_package_name)
                    continue

                test_info = MonkeyReportGenerator.TestInformation(self._device_serial, self._param_dict)
                issue_detail, issue_loops = self.get_issue_detail(bug, test_info)

                add_result = False
                jira_key = "error_jira_key" + str(time())
                try:
                    add_result = BugDao.add_bug_record(bug.bug_signature_code, '', self.tag)
                    print "add result: " + str(add_result)
                    jira_summary = ""
                    jira_assignee = ""
                    if add_result:
                        try:
                            jira_key, jira_summary, jira_assignee = self.create_new_jira(bug, issue_detail)
                        except Exception, why:
                            print "create new jira error: ", why
                            BugDao.delete_record_from_bug_jira_table(bug.bug_signature_code)

                        if "error_jira_key" not in jira_key:
                            if not BugDao.add_jira_key_to_bug_record(bug.bug_signature_code, jira_key):
                                BugDao.delete_record_from_bug_jira_table(bug.bug_signature_code)
                            BugDao.save_jira(jira_key, jira_summary, jira_assignee, self.tag)
                        else:
                            LogUtil.log("Create new jira error.........")
                            BugDao.delete_record_from_bug_jira_table(bug.bug_signature_code)

                        self.add_watchers(jira_key, self._param_dict[ISSUE_WATCHERS])
                except Exception, why:
                    print "Other error in create, save jira or add watchers: ", why

                if not add_result:
                    retry_times = 3
                    bug_jira = None
                    while retry_times > 0:
                        bug_jira = BugDao.get_by_signature(BugJira, bug.bug_signature_code)
                        try:
                            bug_jira = bug_jira.get()
                        except DoesNotExist:
                            bug_jira = None

                        if bug_jira is not None and bug_jira.jira_id != "":
                            jira_key = bug_jira.jira_id
                            if MonkeyJiraUtil().is_can_reopen_issue(jira_key):
                                MonkeyJiraUtil().change_issue_to_reopen(jira_key)
                            self.add_comment(jira_key, issue_detail)
                            break

                        sleep(SLEEP_TIME_2MIN)
                        retry_times -= 1

                    if bug_jira is None or bug_jira.jira_id == "":
                        jira_key = "error_jira_key_add_comment_" + str(time())
                        LogUtil.log("Add comment error.......")

                self.jira_keys.append(jira_key)
                self.add_attachments(jira_key, bug.bug_signature_code, self.tag, issue_loops)
        else:
            print "There is no bug found!!"

        LogUtil.log_end("create_jira_or_add_comment")
        pass

    def create_new_jira(self, bug, issue_detail):
        LogUtil.log_start("create_new_jira")
        summary = JiraMonkeySummaryTemplate().substitute(bug_type=bug.bug_type,
                                                         is_auto='[ Auto Test ]' if self._is_auto_test else '',
                                                         bug_summary=bug.bug_summary)
        description = issue_detail
        jira_util = MonkeyJiraUtil()
        jira_util.jira_content.set_affects_versions(self._rom_version)
        jira_util.jira_content.set_device_name(self._device_name)
        component, assignee = get_component_assignee(bug.bug_package_name)
        print "assignee", assignee
        if component is not None:
            jira_util.jira_content.set_component(component)
        if assignee is None:
            _assignee = self._param_dict[TESTER].rstrip()
            if _assignee == "":
                _assignee = ISSUE_DEFAULT_OWNER
            jira_util.jira_content.set_assignee(_assignee)
        else:
            jira_util.jira_content.set_assignee(assignee)
        jira_util.jira_content.set_summary(summary)
        jira_util.jira_content.set_description(description)
        reproductivity = self.get_reproductivity(bug.bug_signature_code)
        jira_util.jira_content.set_reproductivity(reproductivity)
        try:
            jira_result = jira_util.create_monkey_task()
            jira_key = jira_result.get('key')
        except (KeyError, ValueError):
            print "create jira error"
            jira_key = "error_jira_key_create_jira_" + str(time())

        if jira_key is None:
            jira_key = "error_jira_key_create_jira_" + str(time())
        print "jira_key", jira_key
        LogUtil.log_end("create_new_jira")
        return jira_key, jira_util.jira_content.summary, jira_util.jira_content.assignee

    @classmethod
    def add_watchers(cls, jira_key, watchers):
        LogUtil.log_start("add_watchers: " + str(watchers))
        if "error_jira_key" in jira_key:
            LogUtil.log("error jira key")
            return
        if watchers is None or watchers == "None":
            return
        watchers_list = watchers.split(',')
        jira_util = MonkeyJiraUtil()
        for watcher in watchers_list:
            print "adding watcher: " + watcher
            if watcher is None or watcher == "None":
                continue
            jira_util.add_watchers(jira_id_or_key=jira_key, watchers=watcher)
        LogUtil.log_end("add_watchers: " + str(watchers))
        pass

    @classmethod
    def add_comment(cls, jira_key, issue_detail):
        LogUtil.log_start("add_comment")
        if "error_jira_key" in jira_key:
            LogUtil.log("error jira key")
            return
        comment = issue_detail
        jira_util = MonkeyJiraUtil()
        jira_util.add_comment(jira_id_or_key=jira_key, comment=comment)
        LogUtil.log_end("add_comment")
        pass

    def add_attachments(self, jira_key, bug_signature_code, tag, issue_loops):
        LogUtil.log_start("add_attachments")
        if "error_jira_key" in jira_key:
            LogUtil.log("error jira key")
            return
        # upload bug file
        bug_files = BugDao.get_by_signature_tag(BugFile, bug_signature_code=bug_signature_code, tag=tag)
        jira_util = MonkeyJiraUtil()
        if bug_files is not None:
            bug_files_all = list()
            for bug_file in bug_files:
                bug_files_all = bug_files_all + bug_file.file_name.split(",")
            bug_files = list(set(bug_files_all))
            for file_name in bug_files:
                print "uploading file: " + file_name
                file_name = self.get_valid_file_name(file_name)
                if file_name is False:
                    continue
                jira_util.add_attachment(jira_id_or_key=jira_key,
                                         file_names=file_name)
        else:
            print "There is no bug report need uploading"

        # upload mapping file
        mapping_file_name = self.CURRENT_PATH + "/mapping.txt"
        if os.path.exists(mapping_file_name):
            jira_util.add_attachment(jira_id_or_key=jira_key, file_names=mapping_file_name)
        else:
            print "There is no mapping file need uploading"

        # upload monkey log file
        for loop in issue_loops:
            file_name = self._log_out_path + "/" + self._log_file_name_origin.format(str(loop))
            print "uploading {} monkey log file: {}".format(str(loop), file_name)
            file_name = self.get_valid_file_name(file_name)
            if file_name is False:
                continue
            jira_util.add_attachment(jira_id_or_key=jira_key,
                                     file_names=file_name)

        LogUtil.log_end("add_attachments")
        pass

    @classmethod
    def is_file_valid(cls, file_name):
        if type(file_name).__name__ != "unicode":
            file_name = unicode(file_name, 'utf8')
        file_size = os.path.getsize(file_name)
        file_size = file_size / float(1024 * 1024)
        file_size = round(file_size, 2)
        return file_size <= 20

    @classmethod
    def get_valid_file_name(cls, file_name):
        if cls.is_file_valid(file_name):
            return file_name
        else:
            zip_file_name = cls.compress_file(file_name)
            if cls.is_file_valid(zip_file_name):
                return zip_file_name
            else:
                return False

    @classmethod
    def compress_file(cls, file_name):
        LogUtil.log_start("compress_file")
        modes = {zipfile.ZIP_DEFLATED: 'deflated', zipfile.ZIP_STORED: 'stored'}
        zip_file_name = file_name + ".zip"
        print('creating archive: ' + zip_file_name)
        zf = zipfile.ZipFile(zip_file_name, mode='w')
        try:
            print('adding ' + file_name + ' with compression mode ' + str(modes[compression]))
            zf.write(file_name, compress_type=compression)
        finally:
            zf.close()
            LogUtil.log_end("compress_file")
            return zip_file_name

    def get_bugs(self):
        bugs = list()
        bug_tag_list = BugDao.get_by_tag(BugTag, self.tag)
        if bug_tag_list is None:
            return None
        else:
            for bug_tag in bug_tag_list:
                bug = BugDao.get_by_signature(Bugs, bug_tag.bug_signature_code)
                if bug is not None:
                    try:
                        bugs.append(bug.get())
                    except DoesNotExist:
                        LogUtil.log("Some error on getting bug: " + bug_tag.bug_signature_code)
        return bugs
        pass

    def get_seed_str(self, bug_signature_code):
        return str(self.bug_seed[bug_signature_code])
        pass

    def collect_bug_seed_info(self, bug_signature_code):
        if bug_signature_code not in self.bug_seed.keys():
            self.bug_seed[bug_signature_code] = [self._seed]
        elif self._seed not in self.bug_seed[bug_signature_code]:
            self.bug_seed[bug_signature_code].append(self._seed)
        pass

    def collect_bug_time_info(self, bug_signature_code, bug_time):
        time_year = self.get_time_year(bug_time)
        bug_time = time_year + "-" + bug_time
        # collecting bug fst time
        if self.result_monkey_issue_fst_time not in self.results_monkey_time[self.current_index].keys():
            self.results_monkey_time[self.current_index][self.result_monkey_issue_fst_time] = dict()
        if bug_signature_code not in self.results_monkey_time[self.current_index][self.result_monkey_issue_fst_time].keys():
            self.results_monkey_time[self.current_index][self.result_monkey_issue_fst_time][bug_signature_code] = bug_time
        else:
            self.results_monkey_time[self.current_index][self.result_monkey_issue_fst_time][bug_signature_code] = \
                self.get_previous_time(
                    self.results_monkey_time[self.current_index][self.result_monkey_issue_fst_time][bug_signature_code],
                    bug_time)

        # collecting bug times
        if self.result_monkey_issue_times not in self.results_monkey_time[self.current_index].keys():
            self.results_monkey_time[self.current_index][self.result_monkey_issue_times] = dict()
        if bug_signature_code not in self.results_monkey_time[self.current_index][self.result_monkey_issue_times].keys():
            self.results_monkey_time[self.current_index][self.result_monkey_issue_times][bug_signature_code] = 1
        else:
            self.results_monkey_time[self.current_index][self.result_monkey_issue_times][bug_signature_code] += 1
        pass

    def get_time_year(self, bug_time):
        time_year = self.results_monkey_time[self.current_index][self.result_monkey_start_time_field].split("-")[0]
        bug_time = time_year + "-" + bug_time
        previous_time = self.get_previous_time(self.results_monkey_time[self.current_index][self.result_monkey_start_time_field], bug_time)
        if self.results_monkey_time[self.current_index][self.result_monkey_start_time_field] == previous_time:
            return time_year
        else:
            return str(int(time_year) + 1)
        pass

    @classmethod
    def get_previous_time(cls, time1, time2):
        time_format = "%Y-%m-%d %H:%M:%S.%f"
        _time1 = datetime.datetime.strptime(time1, time_format)
        _time2 = datetime.datetime.strptime(time2, time_format)
        return time1 if _time2 >= _time1 else time2
        pass

    def get_issue_detail(self, bug, test_info):
        monkey_time_detail = ""
        issue_loops = []
        for round_index in range(1, int(self._param_dict[MONKEY_ROUND]) + 1):
            if self.result_monkey_issue_fst_time not in self.results_monkey_time[round_index].keys():
                continue
            elif bug.bug_signature_code not in self.results_monkey_time[round_index][self.result_monkey_issue_fst_time].keys():
                continue

            issue_loops.append(round_index)
            time_detail = JiraIssueTimeDetail().substitute(test_round=round_index,
                                                           monkey_start_time=self.results_monkey_time[round_index][self.result_monkey_start_time_field],
                                                           issue_first_time=self.results_monkey_time[round_index][self.result_monkey_issue_fst_time][bug.bug_signature_code],
                                                           issue_times=str(self.results_monkey_time[round_index][self.result_monkey_issue_times][bug.bug_signature_code])
                                                           )
            monkey_time_detail += time_detail
        test_introduce = AUTO_TEST_INTRODUCTION if self._is_auto_test else RD_TEST_INTRODUCTION.format(tester=self._param_dict[TESTER].rstrip())
        description = JiraMonkeyDescriptionTemplate().substitute(test_introduce_title=test_introduce,
                                                                 package=bug.bug_package_name,
                                                                 bug_type=bug.bug_type,
                                                                 device_names=self._device_name,
                                                                 rom_versions=self._rom_version,
                                                                 app_version_name=test_info.app_versions,
                                                                 android_version=test_info.android_version,
                                                                 auto_test_info="| 编译APK的Jenkins ID | Jenkins Job ID of Building apk | " +
                                                                                str(test_info.jenkins_build_num) + " |"
                                                                 if self._is_auto_test else "",
                                                                 monkey_seed=self.get_seed_str(bug.bug_signature_code),
                                                                 monkey_param=test_info.monkey_param,
                                                                 monkey_total_time=test_info.monkey_time,
                                                                 monkey_time_detail=monkey_time_detail,
                                                                 bug_details=bug.bug_detail)
        return description, issue_loops
        pass

    def get_reproductivity(self, bug_signature_code):
        bug_count = 0
        for monkey_round in range(1, int(self._param_dict[MONKEY_ROUND]) + 1):
            if self.result_monkey_issue_times not in self.results_monkey_time[monkey_round].keys():
                continue
            elif bug_signature_code not in self.results_monkey_time[monkey_round][self.result_monkey_issue_times].keys():
                continue
            bug_count += self.results_monkey_time[monkey_round][self.result_monkey_issue_times][bug_signature_code]

        if bug_count == 1:
            return REPRODUCTIVITY_ONCE
        elif bug_count >= 3:
            return REPRODUCTIVITY_EVERY_TIME
        else:
            return REPRODUCTIVITY_SOMETIMES
        pass

    def save_to_kernel_issues(self, bug_signature_code, bug_summary, bug_type, bug_pkg_name):
        if not isinstance(self._kernel_issues, dict):
            self._kernel_issues = dict()

        for monkey_round in range(1, int(self._param_dict[MONKEY_ROUND]) + 1):
            if self.result_monkey_issue_fst_time not in self.results_monkey_time[monkey_round].keys():
                continue
            if bug_signature_code in self.results_monkey_time[monkey_round][self.result_monkey_issue_fst_time].keys():
                # Init self._kernel_issues[monkey_round]
                if monkey_round not in self._kernel_issues.keys():
                    self._kernel_issues[monkey_round] = dict()
                # Save monkey start time
                if self.result_monkey_start_time_field not in self._kernel_issues[monkey_round].keys():
                    self._kernel_issues[monkey_round][self.result_monkey_start_time_field] = str(self.results_monkey_time[monkey_round][self.result_monkey_start_time_field])
                # Init issue field
                if self.result_monkey_issue_fst_time not in self._kernel_issues[monkey_round].keys():
                    self._kernel_issues[monkey_round][self.result_monkey_issue_fst_time] = dict()
                    self._kernel_issues[monkey_round][self.result_monkey_issue_times] = dict()
                    self._kernel_issues[monkey_round][self.result_monkey_issue_summary] = dict()
                # Save issue fst time
                self._kernel_issues[monkey_round][self.result_monkey_issue_fst_time][bug_signature_code] = self.results_monkey_time[monkey_round][self.result_monkey_issue_fst_time][bug_signature_code]
                # Save issue times
                self._kernel_issues[monkey_round][self.result_monkey_issue_times][bug_signature_code] = self.results_monkey_time[monkey_round][self.result_monkey_issue_times][bug_signature_code]
                # Save issue summary
                self._kernel_issues[monkey_round][self.result_monkey_issue_summary][bug_signature_code] = "[ {} ][ {} ]{}".format(bug_pkg_name, bug_type, bug_summary)
        pass

    def save_to_not_submitted_issues(self, bug_signature_code, bug_time, bug_type, bug_summary, bug_pkg_name):
        if not isinstance(self._not_submitted_issues, dict):
            self._not_submitted_issues = dict()
        if self.current_index not in self._not_submitted_issues.keys():
            self._not_submitted_issues[self.current_index] = dict()
        if self.result_monkey_start_time_field not in self._not_submitted_issues[self.current_index].keys():
            self._not_submitted_issues[self.current_index][self.result_monkey_start_time_field] = str(self.results_monkey_time[self.current_index][self.result_monkey_start_time_field])
        if self.result_monkey_issue_fst_time not in self._not_submitted_issues[self.current_index].keys():
            self._not_submitted_issues[self.current_index][self.result_monkey_issue_fst_time] = dict()
            self._not_submitted_issues[self.current_index][self.result_monkey_issue_times] = dict()
            self._not_submitted_issues[self.current_index][self.result_monkey_issue_summary] = dict()

        if bug_signature_code not in self._not_submitted_issues[self.current_index][self.result_monkey_issue_fst_time].keys():
            self._not_submitted_issues[self.current_index][self.result_monkey_issue_fst_time][bug_signature_code] = bug_time
            self._not_submitted_issues[self.current_index][self.result_monkey_issue_times][bug_signature_code] = 1
            self._not_submitted_issues[self.current_index][self.result_monkey_issue_summary][bug_signature_code] = "[ {} ][ {} ]{}".format(bug_pkg_name, bug_type, bug_summary)
        else:
            self._not_submitted_issues[self.current_index][self.result_monkey_issue_times][bug_signature_code] += 1

        pass

    def is_apk_in_device_belong_normal_key(self):
        apk_in_device_file_path = ADBUtil.get_apk_file_path(self._device_serial, self.test_apk_package)
        ADBUtil.root_and_remount(self._device_serial)
        output_apk = os.path.basename(apk_in_device_file_path)
        ADBUtil.pull(self._device_serial, apk_in_device_file_path, ".")
        output_apk_md5 = SignAPKUtil.get_md5_if_belong_normal_key(output_apk)
        return output_apk_md5 != ""
        pass

# if __name__ == "__main__":
#     file_name = "/Users/may/Downloads/riva_8.12.21_261152.zip"
#     package = "com.mi.android.globallauncher"
#     monkey = MonkeyApkTester()
#     monkey.analysis_bug_result(file_name, package)
