from utils.LogUtil import LogUtil
from monkeyTest.MonkeyApkTester import MonkeyApkTester


class proxy:
    _run = None
    _rst = False

    def __init__(self, run):
        LogUtil.log_start("__init__")
        self._run = run

    def do_script(self):
        LogUtil.log_start("doScript")

        LogUtil.log_start("PrivacyFullTester")

        _MonkeyApkTester = MonkeyApkTester(self._run._serial, self._run._out_path, self._run._param_dict)
        _MonkeyApkTester.run_test()

        self._rst = True

        LogUtil.log_end("PrivacyFullTester")

    def get_result(self):
        return self._rst
