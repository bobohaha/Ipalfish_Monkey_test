import os


class PathUtil:

    _current_path = ""
    _file_path = ""

    def __init__(self, file):
        self._current_path = os.getcwd()
        self._file_path = os.path.dirname(os.path.realpath(file))

    def chdir_here(self):
        os.chdir(self._file_path)

    def back(self):
        os.chdir(self._current_path)

    @staticmethod
    def get_file_path(file):
        # __file__
        return os.path.dirname(os.path.realpath(file))

    @staticmethod
    def chdir(file_path):
        os.chdir(file_path)









