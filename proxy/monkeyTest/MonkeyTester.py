from proxy.Util.log_util import LogUtil
from proxy.Util.adb_util import ADBUtil
from proxy.Util.kill_process_util import KillProcessUtil
from proxy.Util.device_uitl import DeviceUtil
from proxy.Util.path_util import PathUtil
from proxy.param import *
import time
import os
import sys


class MonkeyTester:
    monkey_round_maximum_time_min = 5
    _log_file_name = "monkey_log.txt"
    _monkey_command = ""
    _seed = None

    def __init__(self, _serial, _path):
        self.device_serial = _serial
        self.out_path = _path
        pass

    def run(self):
        self.run_monkey()
        pass

    def run_monkey(self):
        LogUtil.log_start("test: run monkey")
        self.run_monkey_in_background()
        # running_time = self.hold_for_monkey_run_time()
        self.kill_monkey()

    def kill_monkey(self):

        LogUtil.log_start("kill_monkey")

        KillProcessUtil.kill_device_process(self.device_serial, "monkey")

        LogUtil.log_end("kill_monkey")

    def run_monkey_in_background(self):
        LogUtil.log_start("run_monkey_in_background")

        self.init_monkey_command()
        ADBUtil.execute_shell(self.device_serial, self._monkey_command)

        LogUtil.log_end("run_monkey_in_background")

    def into_test_activity(self):
        command = ' am start -n ' + self.get_ai_activity()
        ADBUtil.execute_shell(self.device_serial, command)
        pass

    def get_ai_activity(self):
        return AI_CLASS_ROOM_ACTIVITY
        pass

    def hold_for_monkey_run_time(self):
        LogUtil.log_start("hold_for_monkey_run_time")

        start_time = time.time()
        monkey_max_time = int(self.monkey_round_maximum_time_min) * 60

        LogUtil.log("hold_for_monkey_run_time(): monkey_round_maximum_time_min is " + str(self.monkey_round_maximum_time_min))

        try:
            android_sdk = int(ADBUtil.get_prop(self.device_serial, 'ro.build.version.sdk'))
        except Exception:
            android_sdk = 24
        while True:
            left_seconds = start_time + monkey_max_time - time.time()
            if left_seconds <= 0:
                break
            LogUtil.log("hold_for_monkey_run_time(): left {} minutes...".format(str(left_seconds / 60)))
            time.sleep(2)
            # Set to volume down to prevent noise in lab.
            self.set_volume_down(android_version=android_sdk)
            if ADBUtil.get_process_id_by_name(self.device_serial, "monkey") is None:
                self.run_monkey_in_background()

        end_time = time.time()

        LogUtil.log_end("hold_for_monkey_run_time")

        return end_time - start_time

    def init_monkey_command(self):
        LogUtil.log_start("init_monkey_command")
        log_file_full_path = self.out_path + "/" + self._log_file_name
        command = MONKEY_COMMAND + " " + PACKAGE_NAME + " "

        self.get_seed()
        if self._seed is not None:
            command = command + "-s " + self._seed + " "
        else:
            command = command + "-s " + "1 "
        command = command + " 50000 > " + log_file_full_path + " & "
        self._monkey_command = command
        LogUtil.log_end("init_monkey_command")

    def get_seed(self):

        log_file_full_path = self.out_path + "/" + self._log_file_name
        if self._log_file_name != "" and os.path.exists(log_file_full_path):
            log_file = open(log_file_full_path, 'r')
            for line in log_file:
                if ":Monkey:" in line:
                    self._seed = line.split("seed=")[1].split(" ")[0]
                    return
        else:
            self._seed = None

    def set_volume_down(self, android_version=26):
        if android_version <= 25:
            # call audio method 3 and set media volume (3) down to 1 (minimum volume)
            ADBUtil.execute_shell(self.device_serial, 'service call audio 3 i32 3 i32 1')
        else:
            # Set media (3) volume down to 1 (minimum volume)
            std_out, std_err = ADBUtil.execute_shell(self.device_serial, 'media volume --stream 3 --get', output=True)
            import re
            find_volume = re.search('volume is (\\d+) ', std_out)
            if find_volume is not None and int(find_volume.group(1)) > 1:
                ADBUtil.execute_shell(self.device_serial, 'media volume --stream 3 --set 1', output=False)

    # def get_crash_info(self, filename):
    #     return self.BUG_TYPE_CRASH + re.findall(r"app_crash(.+?)_", filename)[0]
    #
    # def get_anr_info(self, filename):
    #     return self.BUG_TYPE_ANR + re.findall(r"anr_(.+?)_", filename)[0]


if __name__ == '__main__':
    args = sys.argv[1:]
    _MonkeyTest = MonkeyTester(args[0], args[1])
    _MonkeyTest.into_test_activity()
