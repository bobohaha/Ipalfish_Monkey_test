# coding:utf-8
import sys
from proxy.monkeyTest.MonkeyTester import MonkeyTester

if __name__ == '__main__':
    # 接收参数
    args = sys.argv[1:]
    _MonkeyTest = MonkeyTester(args[0], args[1])
    _MonkeyTest.run()

