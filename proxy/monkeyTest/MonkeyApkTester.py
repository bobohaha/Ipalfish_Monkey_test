from proxy.usb.UsbUtil import UsbUtil
from proxy.utils.LogUtil import LogUtil
from proxy.utils.PathUtil import PathUtil
from proxy.utils.ADBUtil import ADBUtil
from proxy.utils.PropUtil import PropUtil

from proxy.utils.KillProcessUtil import KillProcessUtil
from proxy.monkeyTest import xlsxwriter
from proxy.monkeyTest.MonkeyApkSyncUtil import MonkeyApkSyncUtil
from proxy.monkeyTest.MonkeyApkSyncUtil import MonkeyTestApkLocalName
from proxy import param

import os
import re

from time import sleep, time


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
    _rom_info = None
    _rom_version = ""
    _device_name = ""

    results = {}
    bugs = {}

    MONKEY_CHECK_INTERVAL_SECOND = 60

    _MonkeyApkSyncUtil = None

    def __init__(self, serial, out_path, param_dict):
        self._device_serial = serial
        self._log_out_path = out_path
        self._rom_info = param_dict
        self.clear_log_folder()
        self._device_name = PropUtil.get_device_name(serial)
        self._rom_version = PropUtil.get_rom_version(serial)
        self._MonkeyApkSyncUtil = MonkeyApkSyncUtil(self._rom_info[param.PACKAGE_NAME])
        pass

    def download_test_apk(self):
        _PathUtil = PathUtil(__file__)
        _PathUtil.chdir_here()
        self._MonkeyApkSyncUtil.\
            download_objects_with_version(self._rom_info[param.TEST_APK_BUILD_VERSION])
    pass

    def install_downloaded_test_apk(self):
        LogUtil.log_start("install_test_apk")
        self.install_apk(MonkeyTestApkLocalName)
        LogUtil.log_end("install_test_apk")

    def install_test_apk(self):
        LogUtil.log_start("install_test_apk")
        self.install_apk(self._rom_info[param.TEST_APK])
        LogUtil.log_end("install_test_apk")

    def install_apk(self, apk_file_path):
        LogUtil.log_start("install_apk")
        UsbUtil.make_sure_usb_connected(self._device_serial, "0")
        ADBUtil.install(
            self._device_serial, apk_file_path)
        LogUtil.log_end("install_apk")

    def reboot_device(self):
        UsbUtil.make_sure_usb_connected(self._device_serial, "0")
        ADBUtil.reboot(self._device_serial)
        ADBUtil.wait_for_device(self._device_serial)
        ADBUtil.wait_for_reboot_complete(self._device_serial)
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

        round_str = self._rom_info["MONKEY_ROUND"]

        round_count = int(round_str)

        for round_index in range(1, round_count + 1):
            self.test(round_index)

        self.write_excel()
        self.move_result()

        LogUtil.log_end("run_test")

    def test(self, round_index):
        LogUtil.log_start("test: " + str(round_index))
        UsbUtil.make_sure_usb_connected(self._device_serial, "0")
        self.reboot_device()
        UsbUtil.make_sure_usb_connected(self._device_serial, "0")

        self.run_monkey_in_background()
        running_time = self.hold_for_monkey_run_time()
        self.kill_monkey()

        self.pull_log(round_index)
        self.analyze_log(round_index, running_time)
        UsbUtil.make_sure_usb_connected(self._device_serial, "0")
        self.reboot_device()
        UsbUtil.make_sure_usb_connected(self._device_serial, "0")
        LogUtil.log_end("test: " + str(round_index))

    def kill_monkey(self):

        LogUtil.log_start("kill_monkey")

        KillProcessUtil.kill_device_process(self._device_serial, "monkey")

        LogUtil.log_end("kill_monkey")

    def run_monkey_in_background(self):

        LogUtil.log_start("run_monkey_in_background")

        input_package_name = self._rom_info["PACKAGE_NAME"]
        monkey_param = self._rom_info["MONKEY_PARAM"]

        package_name_ary = input_package_name.split(",")
        package_name_str = ""

        for package_name in package_name_ary:
            package_name_str = package_name_str + "-p" + " " + package_name + " "

        self._log_file_name = "_" + str(time())

        log_file_full_path = self._log_out_path + "/" + self._log_file_name

        command = "adb -s " + self._device_serial + " shell monkey " \
                  + monkey_param + " " + package_name_str

        seed_str = self.get_seed()
        if seed_str is not None:
            command = command + "-s " + seed_str + " "

        command = command + "50000000 > " + log_file_full_path + " & "

        LogUtil.log(command)
        os.system(command)

        LogUtil.log_end("run_monkey_in_background")

    def hold_for_monkey_run_time(self):
        LogUtil.log_start("hold_for_monkey_run_time")

        start_time = time()
        monkey_round_maximum_time_min = self._rom_info["MONKEY_ROUND_MAXIMUM_TIME"]
        monkey_max_time = int(monkey_round_maximum_time_min) * 60

        LogUtil.log(
            "hold_for_monkey_run_time(): monkey_round_maximum_time_min is "
            + monkey_round_maximum_time_min)

        while time() - start_time < monkey_max_time:
            LogUtil.log("hold_for_monkey_run_time(): " + str(time()))
            sleep(MonkeyApkTester.MONKEY_CHECK_INTERVAL_SECOND)

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

        seed_str = self.get_seed()

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

        self.results[round_index] = {"seed": seed_str, "times": running_str,
                                     "crash": crash_str, "anr": anr_str}

    def get_seed(self):
        seed_str = self._rom_info["MONKEY_SEED"]
        log_file_full_path = self._log_out_path + "/" + self._log_file_name
        if seed_str is not None and seed_str != "":
            return seed_str
        elif self._log_file_name != "" and os.path.exists(log_file_full_path):
            log_file = open(log_file_full_path, 'r')
            for line in log_file:
                if ":Monkey:" in line:
                    return line.split("seed=")[1].split(" ")[0]
        else:
            return None

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
        if len(self.bugs) == 0:
            worksheet.write(line, 1, "Pass", format_value_center)
        else:
            worksheet.write(line, 1, "Failed", format_value_center)
        line += 1
        worksheet.write(line, 0, 'Run Times*Hours', format_head_title)
        worksheet.write(line, 1, self._rom_info["MONKEY_ROUND"] + "*" + str(
            int(self._rom_info["MONKEY_ROUND_MAXIMUM_TIME"]) / 60) + "hours", format_value_center)
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

        LogUtil.log_end("move_result")

    def analyze_bugs(self, bug_files, bug_type):
        LogUtil.log_start("analyze_bugs")

        result = ""
        for filename in bug_files:
            if filename:
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
