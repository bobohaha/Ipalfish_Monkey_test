import traceback
from BugModel import *


class BugDao:
    def __init__(self):
        pass

    @staticmethod
    def save_bug_detail(bug_detail_dict, tag):
        print "save_bug_detail: ", str(bug_detail_dict), tag
        _bug_summary = bug_detail_dict['summary']
        if len(_bug_summary) > 150:
            _bug_summary = _bug_summary[:150] + "..."

        try:
            _bug = Bugs(bug_detail=bug_detail_dict['det'],
                        bug_signature_code=bug_detail_dict['dgt'],
                        bug_pid=bug_detail_dict['pid'],
                        bug_package_name=bug_detail_dict['pkgName'],
                        bug_summary=_bug_summary,
                        bug_time=bug_detail_dict['time'],
                        bug_type=bug_detail_dict['type'],
                        tag=tag)
        except Exception, why:
            print "Incomplete bug record, error: ", why
            return False, None

        _bug_get_result = BugDao.get(Bugs, Bugs.bug_signature_code == _bug.bug_signature_code)
        try:
            if _bug_get_result is None:
                print "bug detail saving..."
                _bug.save()
            else:
                print "bug detail updating..."
                Bugs.update(_bug.__data__).where(Bugs.bug_signature_code == _bug.bug_signature_code).execute()
            return True, _bug
        except (DoesNotExist, IntegrityError, OperationalError), why:
            print "save bug detail \"" + str(_bug) + "\" error: ", why
            print traceback.format_exc()
            return False, _bug

    @staticmethod
    def save_bug_tag(bug_signature_code, tag):
        print "save_bug_tag: ", bug_signature_code, tag
        _bug_tag = BugTag(bug_signature_code=bug_signature_code,
                          tag=tag)
        _bug_tag_get_result = BugDao.get(BugTag,
                                         BugTag.bug_signature_code == bug_signature_code,
                                         BugTag.tag == tag)
        try:
            if _bug_tag_get_result is None:
                print "bug tag saving..."
                _bug_tag.save()
            else:
                print "bug tag saved..."
            return True, _bug_tag
        except (IntegrityError, DoesNotExist, OperationalError), why:
            print "save bug tag \"" + str(_bug_tag) + "\" error: ", why
            print traceback.format_exc()
            return False, _bug_tag
        pass

    @staticmethod
    def save_bug_rom(bug_signature_code, device_name, jira_miui_model, rom_version, tag):
        print "save_bug_rom: ", bug_signature_code, device_name, jira_miui_model, rom_version, tag
        _bug_rom = BugRom(bug_signature_code=bug_signature_code,
                          device_name=device_name,
                          jira_miui_model=jira_miui_model,
                          rom_version=rom_version,
                          tag=tag)
        _bug_rom_get_result = BugDao.get(BugRom,
                                         BugRom.bug_signature_code == bug_signature_code,
                                         BugRom.device_name == device_name)
        try:
            if _bug_rom_get_result is None:
                print "bug rom saving..."
                _bug_rom.save()
            else:
                print "bug rom updating..."
                BugRom.update(_bug_rom.__data__)\
                    .where(BugRom.bug_signature_code == _bug_rom.bug_signature_code).execute()
            return True, _bug_rom
        except (IntegrityError, DoesNotExist, OperationalError), why:
            print "save bug rom \"" + str(_bug_rom) + "\" error: ", why
            print traceback.format_exc()
            return False, _bug_rom

    @staticmethod
    def save_bug_file(bug_signature_code, file_name, tag):
        print "save_bug_file: ", bug_signature_code, file_name, tag
        try:
            _bug_file, save_result = BugFile.get_or_create(bug_signature_code=bug_signature_code,
                                                           file_name=file_name,
                                                           tag=tag)
            if save_result is False:
                print "bug file save failed: {{bug_signature_code: {0}, file_name: {1}, tag={2}}}".format(bug_signature_code, file_name, tag)
            else:
                print "bug file save successful!!"
            return save_result, _bug_file
        except (IntegrityError, DoesNotExist, OperationalError), why:
            print "bug file save failed: {{bug_signature_code: {0}, file_name: {1}, tag={2}}}, error: {3}".format(bug_signature_code, file_name, tag, why)
            print traceback.format_exc()
            return False, None

    @staticmethod
    def save_jira(jira_id, jira_summary, jira_assignee, tag):
        print "save_jira: ", jira_id, jira_summary, jira_assignee, tag
        _jira_issue = Jiras(jira_id=jira_id,
                            jira_summary=jira_summary,
                            jira_assignee=jira_assignee,
                            tag=tag)
        try:
            _jira_issue_get_result = BugDao.get(Jiras, Jiras.jira_id == jira_id)
            if _jira_issue_get_result is None:
                print "jira saving..."
                _jira_issue.save()
            else:
                print "jira updating..."
                Jiras.update(_jira_issue.__data__).where(Jiras.jira_id == _jira_issue.jira_id).execute()
            return True, _jira_issue
        except (IntegrityError, DoesNotExist, OperationalError), why:
            print "save jira \"" + str(_jira_issue) + "\" error: ", why
            print traceback.format_exc()
            return False, _jira_issue

    @staticmethod
    def save_bug_jira(bug_signature_code, jira_id, tag):
        print "save_bug_jira: ", bug_signature_code, jira_id, tag
        _bug_jira = BugJira(bug_signature_code=bug_signature_code,
                            jira_id=jira_id,
                            tag=tag)
        _bug_jira_get_result = BugDao.get_by_signature(BugJira, bug_signature_code)
        try:
            if _bug_jira_get_result is None:
                print "bug jira saving..."
                _bug_jira.save()
            else:
                print "bug jira updating..."
                BugJira.update(_bug_jira.__data__)\
                    .where(BugJira.bug_signature_code == _bug_jira.bug_signature_code).execute()
            return True, _bug_jira
        except (IntegrityError, DoesNotExist, OperationalError), why:
            print "save bug jira \"" + str(_bug_jira) + "\" error: ", why
            print traceback.format_exc()
            return False, _bug_jira

    @staticmethod
    def get_by_tag(table_name, tag):
        try:
            return BugDao.get(table_name, table_name.tag == tag)
        except DoesNotExist:
            return None

    @staticmethod
    def get_jira_record_by_jira_key(jira_key):
        try:
            return BugDao.get(Jiras, Jiras.jira_id == jira_key).get()
        except (DoesNotExist, AttributeError):
            return None

    @staticmethod
    def get_by_signature(table_name, bug_signature_code):
        try:
            return BugDao.get(table_name, table_name.bug_signature_code == bug_signature_code)
        except DoesNotExist:
            return None

    @staticmethod
    def get_by_signature_tag(table_name, bug_signature_code, tag):
        try:
            return BugDao.get(table_name, table_name.bug_signature_code == bug_signature_code, table_name.tag == tag)
        except DoesNotExist:
            return None

    @classmethod
    def get(cls, table_name, *query, **filters):
        print "BugDao.get(" + table_name.__name__ + "): >>"
        sq = table_name.select()
        if query:
            sq = sq.where(*query)
        if filters:
            sq = sq.filter(**filters)
        try:
            fst_record = sq.get()
            print "sq.get():", fst_record
        except (DoesNotExist, OperationalError), why:
            print "BugDao get method error : ", why
            sq = None
        print "BugDao.get(" + table_name.__name__ + "): <<"
        return sq

    @classmethod
    def update(cls, table_name, __data=None, **kwargs):
        print "update: ", table_name.__name__
        try:
            table_name.update(__data, **kwargs)
            return True
        except (DoesNotExist, OperationalError), why:
            print "{} update error: {}".format(table_name.__name__, why)
            return False

    @staticmethod
    def update_tag_by_signature(table_name, bug_signature_code, tag):
        try:
            table_name.update(tag=tag).where(table_name.bug_signature_code == bug_signature_code).execute()
            return True
        except (DoesNotExist, OperationalError):
            return False

    @staticmethod
    def update_tag_by_issue_id(table_name, issue_id, tag):
        try:
            table_name.update(tag=tag).where(table_name.jira_id == issue_id).execute()
            return True
        except (DoesNotExist, OperationalError):
            return False

    @staticmethod
    def update_jiras_tag_by_jira_id(jira_id, tag):
        return BugDao.update_tag_by_issue_id(Jiras, issue_id=jira_id, tag=tag)

    @classmethod
    def add_bug_record(cls, bug_signature_code, jira_key, tag):
        _bug_record = BugJira(bug_signature_code=bug_signature_code, jira_id=jira_key, tag=tag)
        try:
            _bug_record.save()
            return True
        except IntegrityError, why:
            print "add_bug_record error: ", why
            return False
        pass

    @classmethod
    def add_jira_key_to_bug_record(cls, bug_signature_code, jira_key):
        try:
            BugJira.update(jira_id=jira_key).where(BugJira.bug_signature_code == bug_signature_code).execute()
            return True
        except Exception, why:
            print "add_jira_key_to_bug_record error: ", why
            return False
        pass

    @classmethod
    def delete_record_from_bug_jira_table(cls, bug_signature_code):
        try:
            BugJira.delete().where(BugJira.bug_signature_code == bug_signature_code).execute()
        except Exception, why:
            print "delete_record_from_bug_jira_table error: ", why
        pass


# if __name__ == "__main__":
#     # bugs = [{u'pkgName': u'com.mi.android.globallauncher', u'det': u'----- pid 8999 at 2019-01-08 07:54:42 -----\nCmd line: com.mi.android.globallauncher\n"main" prio=5 tid=1 Native\n  | group="main" sCount=1 dsCount=0 flags=1 obj=0x74b59730 self=0x7a1740dc00\n  | sysTid=2646 nice=-10 cgrp=default sched=0/0 handle=0x7a9c0839a8\n  | state=S schedstat=( 2067011615040 446995985270 3470590 ) utm=171165 stm=35536 core=3 HZ=100\n  | stack=0x7feb8c3000-0x7feb8c5000 stackSize=8MB\n  | held mutexes=\n  kernel: __switch_to+0x8c/0x98\n  kernel: binder_thread_read+0x3e4/0x1240\n  kernel: binder_ioctl_write_read.constprop.37+0x1c8/0x2f8\n  kernel: binder_ioctl+0x1f8/0x688\n  kernel: do_vfs_ioctl+0x708/0x7f0\n  kernel: SyS_ioctl+0x60/0x88\n  kernel: __sys_trace_return+0x0/0x4\n  native: #00 pc 000000000006a498  /system/lib64/libc.so (__ioctl+4)\n  native: #01 pc 0000000000024404  /system/lib64/libc.so (ioctl+136)\n  native: #02 pc 0000000000054ac8  /system/lib64/libbinder.so (android::IPCThreadState::talkWithDriver(bool)+256)\n  native: #03 pc 00000000000558b4  /system/lib64/libbinder.so (android::IPCThreadState::waitForResponse(android::Parcel*, int*)+340)\n  native: #04 pc 0000000000055600  /system/lib64/libbinder.so (android::IPCThreadState::transact(int, unsigned int, android::Parcel const&, android::Parcel*, unsigned int)+224)\n  native: #05 pc 000000000004c380  /system/lib64/libbinder.so (android::BpBinder::transact(unsigned int, android::Parcel const&, android::Parcel*, unsigned int)+144)\n  native: #06 pc 0000000000128ab4  /system/lib64/libandroid_runtime.so (???)\n  native: #07 pc 000000000091bcc4  /system/framework/arm64/boot-framework.oat (Java_android_os_BinderProxy_transactNative__ILandroid_os_Parcel_2Landroid_os_Parcel_2I+196)\n  at android.os.BinderProxy.transactNative(Native method)\n  at android.os.BinderProxy.transact(Binder.java:774)\n  at android.app.IActivityManager$Stub$Proxy.getProviderMimeType(IActivityManager.java:6726)\n  at android.content.ContentResolver.getType(ContentResolver.java:579)\n  at android.content.Intent.resolveType(Intent.java:6853)\n  at android.content.Intent.resolveTypeIfNeeded(Intent.java:6875)\n  at android.app.Instrumentation.execStartActivity(Instrumentation.java:1619)\n  at android.app.Activity.startActivityForResult(Activity.java:4555)\n  at com.miui.home.launcher.Launcher.startActivityForResult(Launcher.java:3830)\n  at com.miui.home.launcher.Launcher.startActivityForResult(Launcher.java:3850)\n  at android.app.Activity.startActivity(Activity.java:4874)\n  at android.app.Activity.startActivity(Activity.java:4842)\n  at com.mi.android.pocolauncher.assistant.cards.shortcut.util.ShortcutUtil.startCalendar(ShortcutUtil.java:395)\n  at com.mi.android.pocolauncher.assistant.cards.shortcut.util.ShortcutUtil.startFunctionActivity(ShortcutUtil.java:302)\n  at com.mi.android.pocolauncher.assistant.cards.shortcut.adapter.ShortcutAdapter.lambda$bindAppEntry$1$ShortcutAdapter(ShortcutAdapter.java:161)\n  at com.mi.android.pocolauncher.assistant.cards.shortcut.adapter.ShortcutAdapter$$Lambda$1.onClick(unavailable:-1)\n  at android.view.View.performClick(View.java:6304)\n  at android.view.View$PerformClick.run(View.java:24803)\n  at android.os.Handler.handleCallback(Handler.java:794)\n  at android.os.Handler.dispatchMessage(Handler.java:99)\n  at android.os.Looper.loop(Looper.java:176)\n  at android.app.ActivityThread.main(ActivityThread.java:6651)\n  at java.lang.reflect.Method.invoke(Native method)\n  at com.android.internal.os.RuntimeInit$MethodAndArgsCaller.run(RuntimeInit.java:547)\n  at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:824)\n\n', u'pid': 2646, u'summary': u'Binder:Proxy.getProviderMimeType\u2190ContentResolver.getType\u2190Intent.resolveType\u2190Intent.resolveTypeIfNeeded', u'dgt': u'224efdcd919a94fd983e97850', u'time': u'01-08 07:54:41.634', u'type': u'crash'}]
#     # for bug in bugs:
#     #     BugDao.save_bug_detail(bug, "com.mi.android.globallauncher,com.xiaomi.midrop_2019-01-23 15:48:39.152051")
#     # bug = BugDao.get_by_signature_tag(table_name=BugFile,
#     #                                   bug_signature_code="224efdcd919a94fd983e97850aba1d3d",
#     #                                   tag="com.mi.android.globallauncher,com.xiaomi.midrop_2019-01-23 15:48:39.152051")
#     # print bug
#     bugs = BugDao.get_by_tag(BugFile, tag="com.mi.android.globallauncher,com.xiaomi.midrop_2019-01-23 15:48:39.152051")
#     print len(bugs)
#     print bugs.get().tag
#     for bug in bugs:
#         print bug
