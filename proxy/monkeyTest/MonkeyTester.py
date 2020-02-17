from proxy.Util.log_util import LogUtil
from proxy.Util.adb_util import ADBUtil
from proxy.Util.kill_process_util import KillProcessUtil
from proxy.Util.device_uitl import DeviceUtil
import time
import os



class MonkeyTester:
    monkey_round_maximum_time_min = 5
    _log_file_name =  "monkey_log.txt"
    _monkey_command = ""
    _seed =  None

    def __init__(self, _serial, _path):
        self._device_serial = _serial
        self._out_path = _path
        pass

    def run(self):
        self.run_monkey()
        pass

    def run_monkey(self):
        LogUtil.log_start("test: run monkey")
        # DeviceUtil.reboot_device(self._device_serial)
        # DeviceUtil.clear_device_log(self._device_serial, self._out_path)
        # ADBUtil.silence_and_disable_notification_in_device(self._device_serial)

        # self.results_monkey_time[self.current_index] = dict()
        # self.results_monkey_time[self.current_index][self.result_monkey_start_time_field] = ADBUtil.get_date_time(self._device_serial)
        self.run_monkey_in_background()
        # running_time = self.hold_for_monkey_run_time()
        self.kill_monkey()

        # self.pull_log(round_index)
        # self.analyze_log(round_index, running_time)
        # self.reboot_device()
        # LogUtil.log_end("test: " + str(round_index))

    def kill_monkey(self):

        LogUtil.log_start("kill_monkey")

        KillProcessUtil.kill_device_process(self._device_serial, "monkey")

        LogUtil.log_end("kill_monkey")

    def run_monkey_in_background(self):
        LogUtil.log_start("run_monkey_in_background")

        self.init_monkey_command()
        ADBUtil.execute_shell(self._device_serial, self._monkey_command)

        LogUtil.log_end("run_monkey_in_background")

    def hold_for_monkey_run_time(self):
        LogUtil.log_start("hold_for_monkey_run_time")

        start_time = time()
        monkey_max_time = int(self.monkey_round_maximum_time_min) * 60

        LogUtil.log("hold_for_monkey_run_time(): monkey_round_maximum_time_min is " + self.monkey_round_maximum_time_min)

        try:
            android_sdk = int(ADBUtil.get_prop(self._device_serial, 'ro.build.version.sdk'))
        except Exception:
            android_sdk = 24
        while True:
            left_seconds = start_time + monkey_max_time - time()
            if left_seconds <= 0:
                break
            LogUtil.log("hold_for_monkey_run_time(): left {} minutes...".format(str(left_seconds / 60)))
            sleep()
            # Set to volume down to prevent noise in lab.
            self.set_volume_down(android_version=android_sdk)
            if ADBUtil.get_process_id_by_name(self._device_serial, "monkey") is None:
                self.run_monkey_in_background()

        end_time = time()

        LogUtil.log_end("hold_for_monkey_run_time")

        return end_time - start_time

    def init_monkey_command(self):
        LogUtil.log_start("init_monkey_command")
        log_file_full_path = self._out_path + "/" + self._log_file_name
        command = "monkey " \
                  + "-v --throttle 300 --pct-touch 30 --pct-motion 20 --pct-nav 20 --pct-majornav 15 --pct-appswitch 5 --pct-anyevent 5 --pct-trackball 0 --pct-syskeys 0 --ignore-crashes --ignore-timeouts --bugreport -p" + " " + "cn.xckj.talk_junior "

        self.get_seed()
        if self._seed is not None:
            command = command + "-s " + self._seed + " "

        command = command + " 50 > " + log_file_full_path + " & "
        self._monkey_command = command
        LogUtil.log_end("init_monkey_command")

    def get_seed(self):

        log_file_full_path = self._out_path + "/" + self._log_file_name
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
            ADBUtil.execute_shell(self._device_serial, 'service call audio 3 i32 3 i32 1')
        else:
            # Set media (3) volume down to 1 (minimum volume)
            std_out, std_err = ADBUtil.execute_shell(self._device_serial, 'media volume --stream 3 --get', output=True)
            import re
            find_volume = re.search('volume is (\\d+) ', std_out)
            if find_volume is not None and int(find_volume.group(1)) > 1:
                ADBUtil.execute_shell(self._device_serial, 'media volume --stream 3 --set 1', output=False)

    # def get_crash_info(self, filename):
    #     return self.BUG_TYPE_CRASH + re.findall(r"app_crash(.+?)_", filename)[0]
    #
    # def get_anr_info(self, filename):
    #     return self.BUG_TYPE_ANR + re.findall(r"anr_(.+?)_", filename)[0]

