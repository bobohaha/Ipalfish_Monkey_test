# coding=utf-8
import os

GIT_URL = "http://v9.git.n.xiaomi.com/global_common/global_ci_util"
PROJECT_NAME = "global-ci-util"


def check_update():
    local_version = get_current_version()
    print('global_ci_util_manager.check_update(): current versio %s' % local_version)
    if local_version is not None:
        # Only upgrade when new version available
        install_command = 'pip2 install --upgrade git+%s#egg=%s' % (
            GIT_URL, PROJECT_NAME)
    else:
        install_command = 'pip2 install git+%s#egg=%s' % (GIT_URL, PROJECT_NAME)

    print('global_ci_util_manager.check_update(): '+install_command)
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
        print('Try with --user: '+install_command)
        os.system(install_command)

    # If fail to use --user, try remove it
    if 'Can not perform a \'--user\' install' in str(error):
        install_command = install_command.replace(' --user', '')
        print('Try without --user: '+install_command)
        os.system(install_command)


def get_current_version():
    try:
        import global_ci_util
        return global_ci_util.__version__
    except Exception, why:
        print("get_current_version error", why)
        return None
