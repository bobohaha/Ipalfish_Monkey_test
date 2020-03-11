# coding:utf-8
from proxy.Util.path_util import PathUtil
import sys
from proxy.monkeyTest.MonkeyTester import MonkeyTester

if __name__ == '__main__':
    # 接收参数
    args = sys.argv[1:]
    log_path = PathUtil.get_current_path()
    _MonkeyTest = MonkeyTester(args[0], log_path)
    _MonkeyTest.run()

