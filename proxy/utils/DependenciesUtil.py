import os
from proxy.utils.PathUtil import PathUtil


class DependenciesUtil:
    def __init__(self):
        pass

    @staticmethod
    def install_dependencies():
        file_path = PathUtil.get_file_path(__file__)
        requirements_file_path = file_path + "/requirements.txt"

        command = "pip install -r " + requirements_file_path
        print requirements_file_path
        os.system(command)
