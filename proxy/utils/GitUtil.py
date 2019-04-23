import os


class GitUtil:

    def __init__(self):
        pass

    @staticmethod
    def force_clone(git_site, folder_name):

        if os.path.exists(folder_name):
            command = "rm -rf " + folder_name
            os.system(command)

        command = "git clone " + git_site
        os.system(command)

    @staticmethod
    def clone_if_no_exist(git_site, folder_name):

        if os.path.exists(folder_name):
            return

        command = "git clone " + git_site
        os.system(command)

# @staticmethod
    # def copy_properties(folder):
    #     command = "cp " + GradleUtil.get_properties_path() + " " + folder
    #     print command
    #     os.system(command)
    #
    # @staticmethod
    # def get_properties_path():
    #     return PathUtil.get_file_path(proxy.__file__) + "/local.properties"
    #
    # @staticmethod
    # def clean_assembledebug_assembleAndroidTest():
    #     command = "./gradlew clean assembledebug assembleAndroidTest"
    #     os.system(command)









