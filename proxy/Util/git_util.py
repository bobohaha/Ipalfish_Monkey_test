import os


class git_util:
    def __init__(self):
        pass

    @staticmethod
    def git_clone(_site, _project_name, _branch=None):
        if os.path.exists(_project_name):
            command = "rm -rf " + _project_name
            os.system(command)
        command = "git clone " + _site
        os.system(command)

        if _branch is not None:
            git_branch = "git checkout " + _branch
            os.system(git_branch)
