import datetime
import re
from time import sleep, time
import zipfile
try:
    import zlib
    compression = zipfile.ZIP_DEFLATED
except:
    compression = zipfile.ZIP_STORED

from proxy.utils.BasUtil import BasUtil
from BugDao import BugDao
from BugModel import *
from MonkeyJiraTemplates import *
from MonkeyJiraUtil import *

try:
    import xlsxwriter
except ImportError:
    os.system("pip install XlsxWriter")
    import xlsxwriter

from proxy import param
from proxy.monkeyTest.MonkeyApkSyncUtil import MonkeyApkSyncUtil
from proxy.usb.UsbUtil import UsbUtil
from proxy.utils.ADBUtil import ADBUtil
from proxy.utils.KillProcessUtil import KillProcessUtil
from proxy.utils.LogUtil import LogUtil
from proxy.utils.PathUtil import PathUtil
from proxy.utils.PropUtil import PropUtil


class MonkeyApkTester:
    CURRENT_PATH = PathUtil.get_file_path(__file__)

    OUTPUT_PATH = CURRENT_PATH + "/monkey_log/"
    RESULT_PATH = OUTPUT_PATH + "/result.xlsx"

    OUTPUT_CRASH_PATH = OUTPUT_PATH + "crash/"
    OUTPUT_ANR_PATH = OUTPUT_PATH + "anr/"

    DEVICE_OUTPUT_PATH = "/sdcard/monkeyApkTester_monkey_log/"
    DEVICE_OUTPUT_CRASH_PATH = DEVICE_OUTPUT_PATH + "crash/"
    DEVICE_OUTPUT_ANR_PATH = DEVICE_OUTPUT_PATH + "anr/"

    BUG_TYPE_CRASH = "app_crash"
    BUG_TYPE_ANR = "anr_"

    _device_serial = ""
    _log_out_path = ""
    _log_file_name = ""
    _param_dict = None
    _rom_version = ""
    _device_name = ""
    _is_auto_test = False
    _monkey_command = ""

    results = {}
    bugs = {}

    MONKEY_CHECK_INTERVAL_SECOND = 60

    _MonkeyApkSyncUtil = None

    _rst = None

    def __init__(self, serial, out_path, param_dict):
        self._device_serial = serial
        self._log_out_path = out_path
        self._param_dict = param_dict
        self._is_auto_test = True if self._param_dict[param.TEST_APK_BUILD_VERSION] != "None" else False
        self._seed = None
        self._seed_specify = param_dict["MONKEY_SEED"] if 'MONKEY_SEED' in param_dict.keys() \
                                                          and param_dict['MONKEY_SEED'] is not None \
                                                          and param_dict['MONKEY_SEED'] != "None" \
                                                          and param_dict['MONKEY_SEED'] != "" \
                                                          and param_dict['MONKEY_SEED'] != " " else None
        self.clear_log_folder()
        self._device_name = PropUtil.get_device_name(serial)
        self._rom_version = PropUtil.get_rom_version(serial)
        self._MonkeyApkSyncUtil = MonkeyApkSyncUtil(self._param_dict[param.PACKAGE_NAME])
        self.tag = param_dict['PACKAGE_NAME'] + "_" + str(datetime.datetime.now())
        pass

    def download_test_apk(self):
        if not self._is_auto_test:
            return
        LogUtil.log_start("download_test_apk")
        _PathUtil = PathUtil(__file__)
        _PathUtil.chdir_here()
        self._MonkeyApkSyncUtil. \
            download_objects_with_version(self._param_dict[param.TEST_APK_BUILD_VERSION])
        LogUtil.log_end("download_test_apk")

    def install_downloaded_test_apk(self):
        if not self._is_auto_test:
            return
        LogUtil.log_start("install_downloaded_test_apk")
        test_apk_file_name = self.get_file_name(".apk")
        self.install_apk(test_apk_file_name)
        LogUtil.log_end("install_downloaded_test_apk")

    def install_apk(self, apk_file_path):
        LogUtil.log_start("install_apk")
        UsbUtil.make_sure_usb_connected(self._device_serial, "0")
        self._rst = ADBUtil.try_install(
            self._device_serial, apk_file_path)
        LogUtil.log_end("install_apk")

    def reboot_device(self):
        UsbUtil.make_sure_usb_connected(self._device_serial, "0")
        ADBUtil.reboot(self._device_serial)
        ADBUtil.wait_for_device(self._device_serial)
        UsbUtil.make_sure_usb_connected(self._device_serial, "0")
        ADBUtil.wait_for_reboot_complete(self._device_serial)
        ADBUtil.wait_for_enter_system(self._device_serial)
        pass

    def clear_log_folder(self):
        if os.path.exists(MonkeyApkTester.OUTPUT_PATH):
            command = "rm -rf " + MonkeyApkTester.OUTPUT_PATH
            print command
            os.system(command)

        ADBUtil.rm(self._device_serial, MonkeyApkTester.DEVICE_OUTPUT_PATH)

        if os.path.exists(self._log_out_path):
            command = "rm -rf " + self._log_out_path
            print command
            os.system(command)

        command = "mkdir -p " + self._log_out_path
        print command
        os.system(command)

    def run_test(self):
        LogUtil.log_start("run_test")
        self._rst = False
        round_str = self._param_dict["MONKEY_ROUND"]

        round_count = int(round_str)

        for round_index in range(1, round_count + 1):
            self.test(round_index)

        self.create_jira_or_add_comment()
        self.analyze_result()
        self.write_excel()
        self.move_result()
        LogUtil.log_end("run_test")

    def test(self, round_index):
        LogUtil.log_start("test: " + str(round_index))
        self.reboot_device()
        self.clear_device_log()
        ADBUtil.silence_and_disable_notification_in_device(self._device_serial)

        self.init_monkey_command()
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
        input_package_name = self._param_dict["PACKAGE_NAME"]
        monkey_param = self._param_dict["MONKEY_PARAM"]

        package_name_ary = input_package_name.split(",")
        package_name_str = ""

        for package_name in package_name_ary:
            package_name_str = package_name_str + "-p " + package_name + " "

        self._log_file_name = "_" + str(time())
        log_file_full_path = self._log_out_path + "/" + self._log_file_name

        command = "adb -s " + self._device_serial + " shell monkey " \
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

        UsbUtil.make_sure_usb_connected(self._device_serial)
        os.system(self._monkey_command)

        LogUtil.log_end("run_monkey_in_background")

    def hold_for_monkey_run_time(self):
        LogUtil.log_start("hold_for_monkey_run_time")

        start_time = time()
        monkey_round_maximum_time_min = self._param_dict["MONKEY_ROUND_MAXIMUM_TIME"]
        monkey_max_time = int(monkey_round_maximum_time_min) * 60

        LogUtil.log(
            "hold_for_monkey_run_time(): monkey_round_maximum_time_min is "
            + monkey_round_maximum_time_min)

        while time() - start_time < monkey_max_time:
            LogUtil.log("hold_for_monkey_run_time(): " + str(time()))
            sleep(MonkeyApkTester.MONKEY_CHECK_INTERVAL_SECOND)
            if ADBUtil.get_process_id_by_name(self._device_serial, "monkey") is None:
                self.run_monkey_in_background()

        end_time = time()

        LogUtil.log_end("hold_for_monkey_run_time")

        return end_time - start_time

    def pull_log(self, round_index):

        ADBUtil.mkdir_p(self._device_serial,
                        MonkeyApkTester.DEVICE_OUTPUT_CRASH_PATH + "round_" + str(
                            round_index) + "/")
        ADBUtil.move(self._device_serial, "/sdcard/app_crash* ",
                     MonkeyApkTester.DEVICE_OUTPUT_CRASH_PATH + "round_" + str(round_index) + "/")
        ADBUtil.move(self._device_serial, "/data/app_crash/traces* ",
                     MonkeyApkTester.DEVICE_OUTPUT_CRASH_PATH + "round_" + str(round_index) + "/")

        command = "mkdir -p " + MonkeyApkTester.OUTPUT_CRASH_PATH
        print command
        os.system(command)
        #
        ADBUtil.pull(self._device_serial,
                     MonkeyApkTester.DEVICE_OUTPUT_CRASH_PATH + "round_" + str(round_index) + "/",
                     MonkeyApkTester.OUTPUT_CRASH_PATH)

        ADBUtil.mkdir_p(self._device_serial,
                        MonkeyApkTester.DEVICE_OUTPUT_ANR_PATH + "round_" + str(round_index) + "/")
        ADBUtil.move(self._device_serial, "/sdcard/anr_* ",
                     MonkeyApkTester.DEVICE_OUTPUT_ANR_PATH + "round_" + str(round_index) + "/")
        ADBUtil.move(self._device_serial, "/data/anr/traces* ",
                     MonkeyApkTester.DEVICE_OUTPUT_ANR_PATH + "round_" + str(round_index) + "/")

        command = "mkdir -p " + MonkeyApkTester.OUTPUT_ANR_PATH
        print command
        os.system(command)
        #
        ADBUtil.pull(self._device_serial,
                     MonkeyApkTester.DEVICE_OUTPUT_ANR_PATH + "round_" + str(round_index) + "/",
                     MonkeyApkTester.OUTPUT_ANR_PATH)
        pass

    def analyze_log(self, round_index, running_time):
        self.get_seed()
        command = "ls " + MonkeyApkTester.OUTPUT_CRASH_PATH + "round_" + str(
            round_index) + "/app_crash*"
        output = os.popen(command)
        result = output.read().strip()

        crash_str = ""
        if not result + "x" == "x":
            file_list = result.split("\n")
            crash_str = self.analyze_bugs(file_list, self.BUG_TYPE_CRASH)
        else:
            pass

        command = "ls " + MonkeyApkTester.OUTPUT_ANR_PATH + "round_" + str(round_index) + "/anr_*"
        output = os.popen(command)
        result = output.read().strip()

        anr_str = ""
        if not result + "x" == "x":
            file_list = result.split("\n")
            anr_str = self.analyze_bugs(file_list, self.BUG_TYPE_ANR)
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
        else:
            self._seed = None

    def write_excel(self):

        if os.path.exists(MonkeyApkTester.RESULT_PATH):
            os.remove(MonkeyApkTester.RESULT_PATH)
        # self.analysis_Bug_data(datas)
        # print self.BUGS

        workbook = xlsxwriter.Workbook(MonkeyApkTester.RESULT_PATH)
        worksheet = workbook.add_worksheet()

        worksheet.set_column("A:A", 20)
        worksheet.set_column("B:B", 20)
        worksheet.set_column("C:C", 20)
        worksheet.set_column("D:D", 35)
        worksheet.set_column("E:E", 35)

        line = 0
        format_value_left = workbook.add_format(
            {'border': 1, 'border_color': 'black', 'align': 'left'})
        format_value_left_wrap = workbook.add_format(
            {'border': 1, 'border_color': 'black', 'align': 'left'})
        format_value_left_wrap.set_text_wrap()
        format_value_center = workbook.add_format(
            {'border': 1, 'border_color': 'black', 'align': 'center'})
        format_head_title = workbook.add_format(
            {'bold': True, 'bg_color': '#FFC000', 'align': 'right', 'border': 1,
             'border_color': 'black'})
        format_head_value = workbook.add_format(
            {'bold': True, 'border': 1, 'border_color': 'black'})

        worksheet.write(line, 0, 'Device', format_head_title)
        worksheet.write(line, 1, self._device_name, format_value_center)
        line += 1
        worksheet.write(line, 0, 'Version', format_head_title)
        worksheet.write(line, 1, self._rom_version, format_value_center)
        line += 1
        worksheet.write(line, 0, 'Test Result', format_head_title)
        if self._rst:
            worksheet.write(line, 1, "Pass", format_value_center)
        else:
            worksheet.write(line, 1, "Failed", format_value_center)
        line += 1
        worksheet.write(line, 0, 'Run Times*Hours', format_head_title)
        worksheet.write(line, 1, self._param_dict["MONKEY_ROUND"] + "*" + str(
            int(self._param_dict["MONKEY_ROUND_MAXIMUM_TIME"]) / 60) + "hours", format_value_center)
        line += 2

        # line = 8
        format_item = workbook.add_format({'bold': True})
        format_item_title = workbook.add_format(
            {'bold': True, 'font_color': '#FFFFFF', 'bg_color': '#2F75B5', 'align': 'center',
             'border': 1, 'border_color': 'black'})
        format_item_case = workbook.add_format(
            {'bold': True, 'bg_color': '#BDD7EE', 'align': 'center', 'border': 1,
             'border_color': 'black'})

        worksheet.write(line, 0, 'Bug Analysis', format_item)
        line += 1
        bug_titles = ['Bug name', 'Count', 'JIRA ID', 'JIRA link']
        for x in range(0, len(bug_titles)):
            worksheet.write(line, x, bug_titles[x], format_item_title)
        line += 1

        for bug in self.bugs:
            worksheet.write(line, 0, bug, format_value_left)
            worksheet.write(line, 1, self.bugs[bug], format_value_center)
            worksheet.write(line, 2, None, format_value_center)
            worksheet.write(line, 3, None, format_value_center)
            line += 1
        line += 1

        # worksheet.write(line,0, 'Bug Analysis',format_item)
        detail_titles = ['Run Count', 'RunTime(min)', 'Seed', 'ANR', 'Crash']
        line += 1
        for x in range(0, len(detail_titles)):
            worksheet.write(line, x, detail_titles[x], format_item_title)
        line += 1

        # #print self.RESULTS
        # for case in self.RESULTS:
        #     #line +=1
        #     merge_line = 'A%s:E%s'%(str(line+1),str(line+1))
        #     worksheet.merge_range(merge_line, case, format_item_case)
        #     interval_count = 1
        #     for num in self.RESULTS[case]:
        #         worksheet.write(line+num,0,num,format_value_center)
        #         worksheet.write(line+num,1,self.RESULTS[case][num]['times'],format_value_center)
        #         worksheet.write(line+num,2,self.RESULTS[case][num]['seed'],format_value_center)
        #         worksheet.write(line+num,3,'\n'.join(self.RESULTS[case][num]['anr']),format_value_left_wrap)
        #         worksheet.write(line+num,4,'\n'.join(self.RESULTS[case][num]['crash']),format_value_left_wrap)
        #         interval_count +=1
        #     line = line + interval_count +1

        for num in self.results:
            worksheet.write(line + num, 0, num, format_value_center)
            worksheet.write(line + num, 1, self.results[num]['times'], format_value_center)
            worksheet.write(line + num, 2, self.results[num]['seed'], format_value_center)
            worksheet.write(line + num, 3, self.results[num]['anr'], format_value_center)
            worksheet.write(line + num, 4, self.results[num]['crash'], format_value_center)

        workbook.close()

    def move_result(self):
        LogUtil.log_start("move_result")

        command = "mv " + MonkeyApkTester.OUTPUT_PATH + " " + self._log_out_path
        print command
        os.system(command)

        command = "mv " + MonkeyApkTester.CURRENT_PATH + "/mapping.txt" + " " + self._log_out_path
        print command
        os.system(command)

        LogUtil.log_end("move_result")

    def analyze_bugs(self, bug_files, bug_type):
        LogUtil.log_start("analyze_bugs")
        print bug_files
        result = ""
        for filename in bug_files:
            if filename:
                self.analysis_bug_bas(filename)
                if self.BUG_TYPE_CRASH == bug_type:
                    bug = self.get_crash_info(filename)
                elif self.BUG_TYPE_ANR == bug_type:
                    bug = self.get_anr_info(filename)

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
        packages = self._param_dict['PACKAGE_NAME'].split(",")
        if not isinstance(packages, list):
            packages = [packages]
        for package in packages:
            self.analyzing_and_saving(file_name, package)
        pass

    def analyzing_and_saving(self, file_name, package):
        bug_results = BasUtil().analysis(file_name, package)
        if isinstance(bug_results, list) and len(bug_results) > 0:
            for bug_res in bug_results:
                bug = BugDao.save_bug_detail(bug_res, tag=self.tag)
                if bug is False:
                    print("Save bug details error")
                    continue
                print BugDao.save_bug_file(bug.bug_signature_code, file_name, self.tag)
                print BugDao.save_bug_rom(bug.bug_signature_code,
                                          self._device_name,
                                          get_miui_model(self._device_name),
                                          self._rom_version,
                                          self.tag)
        else:
            print "there is no bug about {} in {}".format(package, file_name)

    def get_rst(self):
        return self._rst

    def analyze_result(self):
        self._rst = len(self.bugs) == 0

    def clear_device_log(self):
        ADBUtil.rm(self._device_serial, MonkeyApkTester.DEVICE_OUTPUT_PATH)
        pass

    def get_file_name(self, keyword, file_path="./"):
        all_files = os.listdir(file_path)
        for f in all_files:
            if keyword in os.path.basename(f):
                return f
        return ""

    def create_jira_or_add_comment(self):
        bugs = BugDao.get_by_tag(Bugs, self.tag)
        if bugs is not None:
            for bug in bugs:
                bug_jira = BugDao.get_by_signature(BugJira, bug_signature_code=bug.bug_signature_code)
                if bug_jira is None:
                    jira_key = self.create_new_jira(bug)
                    self.add_watchers(jira_key, self._param_dict['ISSUE_WATCHERS'])
                else:
                    jira_key = bug_jira.get().jira_id
                    if MonkeyJiraUtil().is_can_reopen_issue(jira_key):
                        MonkeyJiraUtil().change_issue_to_reopen(jira_key)
                    self.add_comment(jira_key, bug)

                self.add_attachments(jira_key, bug.bug_signature_code, self.tag)
                BugDao.save_bug_jira(bug.bug_signature_code, jira_key, self.tag)
        else:
            print "There is no bug found!!"
        pass

    def create_new_jira(self, bug):
        summary = JiraMonkeySummaryTemplate().substitute(bug_type=bug.bug_type,
                                                         bug_summary=bug.bug_summary)
        description = JiraMonkeyDescriptionTemplate().substitute(package=bug.bug_package_name,
                                                                 bug_type=bug.bug_type,
                                                                 device_names=self._device_name,
                                                                 rom_versions=self._rom_version,
                                                                 bug_details=bug.bug_detail)
        jira_util = MonkeyJiraUtil()
        jira_util.jira_content.set_affects_versions(self._rom_version)
        jira_util.jira_content.set_device_name(self._device_name)
        component, assignee = get_component_assignee(self._param_dict['PACKAGE_NAME'])
        print "assignee", assignee
        if component is not None:
            jira_util.jira_content.set_component(component)
        if assignee is None:
            jira_util.jira_content.set_assignee(ISSUE_DEFAULT_OWNER)
        else:
            jira_util.jira_content.set_assignee(assignee)
        jira_util.jira_content.set_summary(summary)
        jira_util.jira_content.set_description(description)
        jira_result = jira_util.create_monkey_task()
        jira_key = jira_result.get('key')
        print jira_key
        return jira_key

    def add_watchers(self, jira_key, watchers):
        if watchers is None:
            return
        watchers_list = watchers.split(',')
        jira_util = MonkeyJiraUtil()
        for watcher in watchers_list:
            print "adding watcher: " + watcher
            if watcher is None:
                continue
            jira_util.add_watchers(jira_id_or_key=jira_key, watchers=watcher)
        pass

    def add_comment(self, jira_key, bug):
        comment = JiraCommentTemplate().substitute(package=bug.bug_package_name,
                                                   bug_type=bug.bug_type,
                                                   device_names=self._device_name,
                                                   rom_versions=self._rom_version,
                                                   bug_details=bug.bug_detail)
        jira_util = MonkeyJiraUtil()
        jira_util.add_comment(jira_id_or_key=jira_key, comment=comment)
        pass

    def add_attachments(self, jira_key, bug_signature_code, tag):
        bug_files = BugDao.get_by_signature_tag(BugFile,
                                                bug_signature_code=bug_signature_code,
                                                tag=tag)
        jira_util = MonkeyJiraUtil()
        if bug_files is not None:
            for bug_file in bug_files:
                print "uploading file: " + bug_file.file_name
                file_name = self.get_valid_file_name(bug_file.file_name)
                if file_name is False:
                    continue
                jira_util.add_attachment(jira_id_or_key=jira_key,
                                         file_names=file_name)
        else:
            print "There is no bug report need uploading"

        mapping_file_name = MonkeyApkTester.CURRENT_PATH + "/mapping.txt"
        if os.path.exists(mapping_file_name):
            jira_util.add_attachment(jira_id_or_key=jira_key, file_names=mapping_file_name)

        else:
            print "There is no mapping file need uploading"
        pass

    def is_file_valid(self, file_name):
        if type(file_name).__name__ != "unicode":
            file_name = unicode(file_name, 'utf8')
        file_size = os.path.getsize(file_name)
        file_size = file_size/float(1024 * 1024)
        file_size = round(file_size, 2)
        return file_size <= 20

    def get_valid_file_name(self, file_name):
        if self.is_file_valid(file_name):
            return file_name
        else:
            zip_file_name = self.compress_file(file_name)
            if self.is_file_valid(zip_file_name):
                return zip_file_name
            else:
                return False

    def compress_file(self, file_name):
        modes = {zipfile.ZIP_DEFLATED: 'deflated', zipfile.ZIP_STORED: 'stored'}
        zip_file_name = file_name + ".zip"
        print('creating archive: ' + zip_file_name)
        zf = zipfile.ZipFile(zip_file_name, mode='w')
        try:
            print('adding ' + file_name + ' with compression mode ' + str(modes[compression]))
            zf.write(file_name, compress_type=compression)
        finally:
            zf.close()
            return zip_file_name


# if __name__ == "__main__":
#     file_name = "/Users/may/Downloads/riva_8.12.21_261152.zip"
#     package = "com.mi.android.globallauncher"
#     monkey = MonkeyApkTester()
#     monkey.analysis_bug_result(file_name, package)
