import os

from proxy.utils.ShellUtil import ShellUtil
from proxy.utils.PathUtil import PathUtil


class SignAPKUtil:

    def __init__(self):
        pass

    CURRENT_PATH = PathUtil.get_file_path(__file__)

    NORMAL_RELEASE_MD5 = "96:8F:F6:58:47:1C:35:72:ED:D7:3A:BF:C1:58:94:6F"
    NORMAL_PLATFORM_MD5 = "70:14:78:A1:E3:B4:B7:E3:97:8E:A6:94:69:41:0F:13"
    NORMAL_SHARED_MD5 = "BC:74:FB:69:A9:EF:D1:FE:A3:0C:3E:45:D3:2E:A9:B2"
    NORMAL_MEDIA_MD5 = "C3:21:77:F9:2B:B3:BF:CF:C9:01:F5:43:15:07:16:7D"
    NORMAL_KEYS_MD5 = [NORMAL_PLATFORM_MD5, NORMAL_RELEASE_MD5, NORMAL_SHARED_MD5, NORMAL_MEDIA_MD5]

    SIGN_APK_JAR_PATH = CURRENT_PATH + "/signapk.jar"

    RELEASE_PEM_PATH = CURRENT_PATH + "/testkey.x509.pem"
    RELEASE_PK8_PATH = CURRENT_PATH + "/testkey.pk8"

    PLATFORM_PEM_PATH = CURRENT_PATH + "/platform.x509.pem"
    PLATFORM_PK8_PATH = CURRENT_PATH + "/platform.pk8"

    SHARED_PEM_PATH = CURRENT_PATH + "/shared.x509.pem"
    SHARED_PK8_PATH = CURRENT_PATH + "/shared.pk8"

    MEDIA_PEM_PATH = CURRENT_PATH + "/media.x509.pem"
    MEDIA_PK8_PATH = CURRENT_PATH + "/media.pk8"

    @staticmethod
    def get_test_key_apk_if_belong_normal_key(apk_path):
        normal_key_md5 = SignAPKUtil.get_md5_if_belong_normal_key(apk_path)

        if normal_key_md5 == "":
            print "get_test_key_if_belong_normal_key(): Not normal key apk, return original apk."
            return apk_path
        pass

        if normal_key_md5 == SignAPKUtil.NORMAL_RELEASE_MD5:
            print "get_test_key_if_belong_normal_key(): NORMAL_RELEASE_MD5"
            output_path = os.path.join(SignAPKUtil.CURRENT_PATH, "test_release_key.apk")
            SignAPKUtil.sign_apk_by_release_key(apk_path, output_path)
            return output_path
        pass

        if normal_key_md5 == SignAPKUtil.NORMAL_PLATFORM_MD5:
            print "get_test_key_if_belong_normal_key(): NORMAL_PLATFORM_MD5"
            output_path = os.path.join(SignAPKUtil.CURRENT_PATH, "test_platform_key.apk")
            SignAPKUtil.sign_apk_by_platform_key(apk_path, output_path)
            return output_path
        pass

        if normal_key_md5 == SignAPKUtil.NORMAL_SHARED_MD5:
            print "get_test_key_if_belong_normal_key(): NORMAL_SHARED_MD5"
            output_path = os.path.join(SignAPKUtil.CURRENT_PATH, "test_shared_key.apk")
            SignAPKUtil.sign_apk_by_shared_key(apk_path, output_path)
            return output_path
        pass

        if normal_key_md5 == SignAPKUtil.NORMAL_MEDIA_MD5:
            print "get_test_key_if_belong_normal_key(): NORMAL_MEDIA_MD5"
            output_path = os.path.join(SignAPKUtil.CURRENT_PATH, "test_media_key.apk")
            SignAPKUtil.sign_apk_by_media_key(apk_path, output_path)
            return output_path
        pass

    @staticmethod
    def is_belong_normal_key(apk_path):
        normal_key_md5 = SignAPKUtil.get_md5_if_belong_normal_key(apk_path)

        if normal_key_md5 == SignAPKUtil.NORMAL_RELEASE_MD5:
            print "is_belong_normal_key(): NORMAL_RELEASE_MD5"
            return True
        pass

        if normal_key_md5 == SignAPKUtil.NORMAL_PLATFORM_MD5:
            print "is_belong_normal_key(): NORMAL_PLATFORM_MD5"
            return True
        pass

        if normal_key_md5 == SignAPKUtil.NORMAL_SHARED_MD5:
            print "is_belong_normal_key(): NORMAL_SHARED_MD5"
            return True
        pass

        if normal_key_md5 == SignAPKUtil.NORMAL_MEDIA_MD5:
            print "is_belong_normal_key(): NORMAL_MEDIA_MD5"
            return True
        pass

        print "is_belong_normal_key(): Not belong normal key"
        return False
        pass

    @staticmethod
    def get_md5_if_belong_normal_key(apk_path):
        # keytool -list -printcert -jarfile fileexplorer_global-20181113-universal.apk | grep MD5 | cut -d ':' -f 2-100
        keytool_command = "keytool -list -printcert -jarfile {}".format(apk_path)
        std_out, std_err = ShellUtil.execute_shell(keytool_command, True)
        apk_md5 = ""
        try:
            for line in std_out.split("\n"):
                if "MD5:" in line:
                    apk_md5 = line.split()[1]
                    print apk_md5

            for md5 in SignAPKUtil.NORMAL_KEYS_MD5:
                if apk_md5 == md5:
                    print "get_md5_if_belong_normal_key(): This apk is belong normal key."
                    return md5
        except Exception, why:
            print "get_md5_if_belong_normal_key(): error->", why
        return ""
        pass

    @staticmethod
    def sign_apk_by_release_key(input_apk_path, output_apk_path):
        sign_command = "java -jar " + SignAPKUtil.SIGN_APK_JAR_PATH + " " + SignAPKUtil.RELEASE_PEM_PATH + " " + SignAPKUtil.RELEASE_PK8_PATH + " " + input_apk_path + " " + output_apk_path
        ShellUtil.execute_shell(sign_command)
        pass

    @staticmethod
    def sign_apk_by_platform_key(input_apk_path, output_apk_path):
        sign_command = "java -jar " + SignAPKUtil.SIGN_APK_JAR_PATH + " " + SignAPKUtil.PLATFORM_PEM_PATH + " " + SignAPKUtil.PLATFORM_PK8_PATH + " " + input_apk_path + " " + output_apk_path
        ShellUtil.execute_shell(sign_command)
        pass

    @staticmethod
    def sign_apk_by_shared_key(input_apk_path, output_apk_path):
        sign_command = "java -jar " + SignAPKUtil.SIGN_APK_JAR_PATH + " " + SignAPKUtil.SHARED_PEM_PATH + " " + SignAPKUtil.SHARED_PK8_PATH + " " + input_apk_path + " " + output_apk_path
        ShellUtil.execute_shell(sign_command)
        pass

    @staticmethod
    def sign_apk_by_media_key(input_apk_path, output_apk_path):
        sign_command = "java -jar " + SignAPKUtil.SIGN_APK_JAR_PATH + " " + SignAPKUtil.MEDIA_PEM_PATH + " " + SignAPKUtil.MEDIA_PK8_PATH + " " + input_apk_path + " " + output_apk_path
        ShellUtil.execute_shell(sign_command)
        pass
