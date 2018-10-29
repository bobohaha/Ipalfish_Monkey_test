import os

from PathUtil import PathUtil
import proxy.proxy

class GradleUtil:

    @staticmethod
    def copy_properties_to(folder):
        command = "cp " + GradleUtil.get_properties_path() + " ./" + folder
        print command
        os.system(command)

    @staticmethod
    def get_properties_path():
        return PathUtil.get_file_path(proxy.__file__) + "/local.properties"

    @staticmethod
    def clean_assembledebug_assembleAndroidTest():
        command = "./gradlew clean assembledebug assembleAndroidTest"
        os.system(command)









