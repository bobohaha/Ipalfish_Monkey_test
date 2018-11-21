from utils.LogUtil import LogUtil
from skipOOBE.SkipOOBE import SkipOOBE
from recoverDevice.DeviceRecover import DeviceRecover
from preSetting.PreSetter import PreSetter
from monkeyTest.MonkeyApkTester import MonkeyApkTester
import param


class proxy:
    _run = None
    _rst = False

    def __init__(self, run):
        LogUtil.log_start("__init__")
        self._run = run

    def do_script(self):
        LogUtil.log_start("doScript")

        # LogUtil.log_start("Recovery Devices for Monkey Test")
        # _DeviceRecover = DeviceRecover(self._run._serial)
        # _DeviceRecover.recover_device()
        # LogUtil.log_end("Recovery Devices for Monkey Test")
        #
        # LogUtil.log_start("Skip OOBE for Monkey Test")
        # test_region_language = {}
        #
        # _SkipOOBE = SkipOOBE(self._run._serial,
        #                      self._run._out_path,
        #                      self._run._param_dict,
        #                      test_region_language)
        # _SkipOOBE.download_or_upgrade_apk()
        # _SkipOOBE.make_sure_in_oobe()
        # _SkipOOBE.install_downloaded_apk()
        # _SkipOOBE.run_test()
        # _SkipOOBE.analyze_result()
        # _SkipOOBE.move_result()
        #
        # if _SkipOOBE.get_result() is False:
        #     LogUtil.log_end("_SkipOOBE fail")
        #     return
        # LogUtil.log_end("Skip OOBE for Monkey Test")

        LogUtil.log_start("Presetting for Monkey Test")
        _PreSetter = PreSetter(self._run._serial,
                               self._run._out_path,
                               self._run._param_dict[param.PACKAGE_NAME])
        _PreSetter.download_or_upgrade_apk()
        _PreSetter.install_downloaded_apk()
        _PreSetter.run_presetting()
        LogUtil.log_end("Presetting for Monkey Test")

        LogUtil.log_start("Monkey Test")

        _MonkeyApkTester = MonkeyApkTester(self._run._serial,
                                           self._run._out_path,
                                           self._run._param_dict)
        _MonkeyApkTester.download_test_apk()
        _MonkeyApkTester.install_downloaded_test_apk()
        _MonkeyApkTester.run_test()

        self._rst = _MonkeyApkTester.get_rst()
        LogUtil.log("Monkey Test Result: " + str(self._rst))

        LogUtil.log_end("Monkey Test")

    def get_result(self):
        return self._rst
