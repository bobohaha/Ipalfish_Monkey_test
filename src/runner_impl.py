# coding:utf-8

from base_runner import BaseRunner
from proxy.proxy import proxy


class RunnerImpl(BaseRunner):

    _proxy = None

    def __init__(self, serial, out_path):
        BaseRunner.__init__(self, serial, out_path)
        self._proxy = proxy(self)

    def on_prepare(self):
        """ 前置条件准备 """
        print 'prepare'

    def on_start(self):
        """
        开始执行
        :return: 无
        """
        self._proxy.do_script()

        pass

    def on_stop(self):
        """
        停止所有已开进程或线程,并返回执行结果
        :return: 执行结果: 成功:True 失败:False
        """
        return self._proxy.get_result()
