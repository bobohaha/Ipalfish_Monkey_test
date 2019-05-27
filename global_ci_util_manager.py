# coding=utf-8
import os
import time

GIT_URL = "http://v9.git.n.xiaomi.com/global_common/global_ci_util"
PROJECT_NAME = "global-ci-util"


def check_update():
    local_version_code = version_code_local()
    git_version_code = version_code_on_git()
    print('global_ci_util_manager.check_update(): current version %s, git version %s' % (
        hex(local_version_code), hex(git_version_code)))
    if git_version_code <= local_version_code:
        # Only upgrade when new version available
        print('global_ci_util_manager.check_update(): not need to update global_ci_util')
        return

    install_command = 'pip2 install --upgrade git+%s#egg=%s' % (GIT_URL, PROJECT_NAME)
    print('global_ci_util_manager.check_update(): ' + install_command)
    from subprocess import Popen, PIPE
    p = Popen(install_command, shell=True, stdout=PIPE,
              stderr=PIPE)
    output, error = p.communicate()
    if len(output) > 0:
        print('-----install result-----\n%s\n------------------------' % output)
    if len(error) > 0:
        print('-----install error-----\n%s\n-----------------------' % error)

    # If fail to install and python suggest to add '--user', try it
    if 'Consider using the `--user`' in str(error):
        install_command = install_command + ' --user'
        print('Try with --user: ' + install_command)
        os.system(install_command)

    # If fail to use --user, try remove it
    if 'Can not perform a \'--user\' install' in str(error):
        install_command = install_command.replace(' --user', '')
        print('Try without --user: ' + install_command)
        os.system(install_command)

    # Sleep for a while to make sure everything ready
    time.sleep(5)


def version_code_local():
    try:
        import global_ci_util
        return global_ci_util.__build__
    except Exception, why:
        print("get_current_version error", why)
        return 0


def version_code_on_git():
    import urllib
    urllib.urlretrieve("%s/raw/master/global_ci_util/version.py" % GIT_URL, "global_ci_version.py")
    import global_ci_version
    return global_ci_version.__build__
