import os
from proxy.Util.path_util import PathUtil


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
        output = os.popen(command)
        status = output.read()

        if "BUILD SUCCESSFUL" not in status:
            print "build fail retry"
            os.popen(command)










