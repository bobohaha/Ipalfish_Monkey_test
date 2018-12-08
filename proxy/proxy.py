from utils.LogUtil import LogUtil
from utils.DependenciesUtil import DependenciesUtil
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
        DependenciesUtil.install_dependencies()
        self._run = run

    def do_script(self):
        LogUtil.log_start("doScript")

        # LogUtil.log_start("Recovery Devices for Monkey Test")
        # _DeviceRecover = DeviceRecover(self._run._serial)
        # _DeviceRecover.recover_device()
        # if _DeviceRecover.get_result() is False:
        #     LogUtil.log_end("Recovery Devices fail")
        #     return
        # LogUtil.log_end("Recovery Devices for Monkey Test")
        #
        # LogUtil.log_start("Skip OOBE for Monkey Test")
        # test_region_language = {}
        # _SkipOOBE = SkipOOBE(self._run._serial,
        #                      self._run._out_path,
        #                      self._run._param_dict,
        #                      test_region_language)
        # _SkipOOBE.download_or_upgrade_apk()
        # _SkipOOBE.make_sure_in_oobe()
        # _SkipOOBE.install_downloaded_apk()
        # if _SkipOOBE.get_result() is False:
        #     LogUtil.log_end("_SkipOOBE fail: install skipOOBE.apk error")
        #     return
        # _SkipOOBE.run_skip_oobe()
        # if _SkipOOBE.get_result() is False:
        #     LogUtil.log_end("_SkipOOBE fail")
        #     return
        # _SkipOOBE.clear_pkg_cache_in_device()
        # LogUtil.log_end("Skip OOBE for Monkey Test")

        LogUtil.log_start("Presetting for Monkey Test")
        _PreSetter = PreSetter(self._run._serial,
                               self._run._out_path,
                               self._run._param_dict[param.PACKAGE_NAME])
        _PreSetter.download_and_push_resources()
        # _PreSetter.download_or_upgrade_apk()
        # _PreSetter.install_downloaded_apk()
        # if _PreSetter.get_result() is False:
        #     LogUtil.log_end("PreSetting error: install presetting apk error!")
        #     return
        # _PreSetter.run_presetting()
        # if _PreSetter.get_result() is False:
        #     LogUtil.log_end("PreSetting error!")
        #     return
        # _PreSetter.clear_pkg_cache_in_device()
        # LogUtil.log_end("Presetting for Monkey Test")
        #
        # LogUtil.log_start("Monkey Test")
        # _MonkeyApkTester = MonkeyApkTester(self._run._serial,
        #                                    self._run._out_path,
        #                                    self._run._param_dict)
        # _MonkeyApkTester.download_test_apk()
        # _MonkeyApkTester.install_downloaded_test_apk()
        # if _MonkeyApkTester.get_rst() is False:
        #     LogUtil.log_end("Monkey Test fail: install test apk of test package error")
        #     return
        # _MonkeyApkTester.run_test()
        #
        # self._rst = _MonkeyApkTester.get_rst()
        # LogUtil.log("Monkey Test Result: " + str(self._rst))
        # LogUtil.log_end("Monkey Test")
        # LogUtil.log_end("doScript")

    def get_result(self):
        return self._rst
