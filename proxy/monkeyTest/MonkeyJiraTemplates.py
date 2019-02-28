# coding=utf-8
from string import Template


BUG_DETAILS = '''
$test_introduce_title
_____________________________________________________________
Bug类型: $bug_type
测试包名: $package
应用版本：$app_version_name
$auto_test_info
设备名称: $device_names
rom版本: $rom_versions
安卓版本：$android_version

seed值: $monkey_seed
monkey命令：$monkey_param
monkey总时长：$monkey_total_time
|  测试轮次  |   monkey开始时间  | issue首次发生时间 |issue发生次数|
$monkey_time_detail
_____________________________________________________________
$bug_details
_____________________________________________________________
有任何问题，请联系yangyamei@xiaomi.com
'''
MONKEY_TIME_DETAIL = "|$test_round|$monkey_start_time|$issue_first_time|$issue_times|\n"

AUTO_TEST_INTRODUCTION = "此为自动化测试的测试结果, 有问题请联系yangyamei@xiaomi.com"
RD_TEST_INTRODUCTION = "此为手动触发monkey测试的测试结果, 有问题请联系{tester}@xiaomi.com"


class JiraMonkeySummaryTemplate(Template):
    def __init__(self):
        Template.__init__(self, '[ Monkey ]$is_auto[ $bug_type ] $bug_summary')
        pass


class JiraMonkeyDescriptionTemplate(Template):
    def __init__(self):
        Template.__init__(self, BUG_DETAILS)


class JiraCommentTemplate(Template):
    def __init__(self):
        Template.__init__(self, BUG_DETAILS)


class JiraIssueTimeDetail(Template):
    def __init__(self):
        Template.__init__(self, MONKEY_TIME_DETAIL)


# if __name__ == "__main__":
#     jira_summary = JiraMonkeyDescriptionTemplate()
#     a = jira_summary.substitute(package='testpkg',
#                                 bug_type="bug",
#                                 device_names="test_dev",
#                                 rom_versions="1.0",
#                                 bug_details='test something')
#     print a
