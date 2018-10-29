# coding:utf-8

from abc import abstractmethod
import json


class BaseRunner:
    _PARAM_CONFIG = 'manifest'

    def __init__(self, serial, out_path):
        """初始化
        :param serial 手机序列号
        :param out_path　输出文件路径
        """
        self._serial = serial
        self._out_path = out_path
        self._param_dict = dict()
        self.__read_param_config(self._PARAM_CONFIG)

    def prepare(self):
        print self.__class__.__name__ + ' preparing ...'
        self.on_prepare()

    def start(self):
        print self.__class__.__name__ + ' starting ...'
        self.on_start()

    def stop(self):
        print self.__class__.__name__ + ' stopping ...'
        return self.on_stop()

    def __read_param_config(self, config_file):
        params = self._read_json_list(config_file)
        if params is None or 0 == len(params):
            print 'Error: The file: ' + config_file + ' is not valid!'
        for item in params:
            self._param_dict[item['name']] = item['value']

    def _read_json_list(self, j_file):
        with open(j_file) as jsons:
            json_list = json.loads(jsons.read())
            return json_list

    def on_prepare(self):
        """ 前置条件准备 """
        pass


    @abstractmethod
    def on_stop(self):
        """
        停止所有已开进程或线程,并返回执行结果
        :return: 执行结果: 成功:True 失败:False
        """
        return False

    @abstractmethod
    def on_start(self):
        """
        开始执行
        :return: 无
        """
        pass
