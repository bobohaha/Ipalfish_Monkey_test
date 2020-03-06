import os
import time


class GitUtil:

    @staticmethod
    def force_clone(git_site, folder_name):

        if os.path.exists(folder_name):
            command = "rm -rf " + folder_name
            os.system(command)

        command = "git clone " + git_site
        os.system(command)
        # time.sleep(5)
        # change_branch_command = "cd TableCheck && git checkout gameFolder"
        # os.system(change_branch_command)

    @staticmethod
    def clone_if_no_exist(git_site, folder_name):

        if os.path.exists(folder_name):
            return

        command = "git clone " + git_site
        os.system(command)
        # time.sleep(5)
        # change_branch_command = "cd TableCheck && git checkout gameFolder"
        # os.system(change_branch_command)










