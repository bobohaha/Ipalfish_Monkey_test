# coding=utf-8
GIT_URL = "http://v9.git.n.xiaomi.com/global_common/global_ci_util"


def check_update():
    import urllib
    urllib.urlretrieve("%s/raw/master/global_ci_util/dependencies_util.py" % GIT_URL, "global_ci_util_installer.py")
    import global_ci_util_installer
    global_ci_util_installer.install_global_ci_util()
