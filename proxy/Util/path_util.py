import os


class PathUtil:

    _current_path = ""
    _file_path = ""

    def __init__(self, file):
        self._current_path = os.getcwd()
        self._file_path = os.path.realpath(file) if os.path.isdir(file) or not os.path.exists(file) else os.path.dirname(os.path.realpath(file))

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

    @staticmethod
    def mkdir_p(file_path, force=False, quiet=False):
        if force:
            command = "rm -rf " + file_path

            if not quiet:
                print command

            os.system(command)

        if not os.path.exists(file_path):
            command = "mkdir -p " + file_path

            if not quiet:
                print command

            os.system(command)

    @staticmethod
    def get_current_path():
        print os.getcwd()









