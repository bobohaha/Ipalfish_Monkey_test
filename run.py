# coding:utf-8

import sys
import os
from xml.dom import minidom

_SUCCESS_FILE = 'success_feedback'


class ManifestXmlParser:

    def __init__(self, name):
        doc = minidom.parse(name)
        self.__root_element = doc.documentElement

    def parse_runner(self):
        elements = self.__root_element.getElementsByTagName('runner')
        if len(elements) != 0:
            Runner.module_name = elements[0].getAttribute('module')
            Runner.class_name = elements[0].getAttribute('class')


class Runner:
    module_name = ''
    class_name = ''

    def __init__(self):
        pass


class Parser:

    def __init__(self):
        pass

    @staticmethod
    def parse_params(arg, key):
        if arg:
            param = arg.split('=')
            if param and len(param) == 2:
                if cmp(key, param[0]) == 0:
                    return param[1]
        return None


if __name__ == '__main__':
    # 接收参数
    args = sys.argv[1:]
    serial = None
    result_path = None
    while len(args) > 0:
        if not serial:
            serial = Parser.parse_params(args[0], 'serial')
        if not result_path:
            result_path = Parser.parse_params(args[0], 'output')
        args = args[1:]
    if serial is None or result_path is None:
        raise Exception('please check whether there have serial and output ? '
                        'maybe you could run: python run.py serial=xxx output=xxx.')
    work_path = os.path.dirname(sys.argv[0])
    if cmp(work_path, '') != 0:
        os.chdir(work_path)

    ManifestXmlParser('manifest.xml').parse_runner()
    if cmp(Runner.module_name, '') == 0 or cmp(Runner.class_name, '') == 0:
        print 'Parse manifest.xml failed!'
        exit(-1)

    print 'Running ' + Runner.class_name + '. Current workspace path: ' + os.getcwd()

    splits = Runner.module_name.split(".")
    if len(splits) > 1:
        runner_module = __import__(name=Runner.module_name, fromlist=[splits[len(splits) -1].strip()])
        RunnerClass = getattr(runner_module, Runner.class_name)
    else:
        runner_module = __import__(name=Runner.module_name)
        RunnerClass = getattr(runner_module, Runner.class_name)
    if not os.path.exists(result_path):
        os.mkdir(result_path)
    runner = RunnerClass(serial, result_path)
    runner.prepare()
    runner.start()
    result = runner.stop()

    if result:
        open(os.path.join(result_path, _SUCCESS_FILE), 'w+').close()
