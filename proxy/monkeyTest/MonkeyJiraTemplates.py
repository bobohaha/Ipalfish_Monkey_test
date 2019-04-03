# coding=utf-8
from string import Template


BUG_DETAILS = '''
$test_introduce_title
_____________________________________________________________
| Bug类型 | Bug Type | $bug_type |
| 测试包名 | Package Name | $package |
| 应用版本 | App Version | $app_version_name |
$auto_test_info
| 设备名称 | Device Name | $device_names |
| Rom版本 | Rom Version | $rom_versions |
| 安卓版本 | Android Version |$android_version |

| Seed值 | Seed | $monkey_seed |
| Monkey命令 | Monkey Command | $monkey_param |
| Monkey总时长 | Monkey Duration | $monkey_total_time |

|  Test Loop  |   Monkey Start Time  | Issue First Time | Issue Times |
$monkey_time_detail
_____________________________________________________________
$bug_details
_____________________________________________________________
有任何问题，请联系yangyamei@xiaomi.com
Any question? Please contact yangyamei@xiaomi.com
'''
MONKEY_TIME_DETAIL = "|$test_round|$monkey_start_time|$issue_first_time|$issue_times|\n"

AUTO_TEST_INTRODUCTION = "此为自动化测试的测试结果, 有问题请联系yangyamei@xiaomi.com\nThis is a test result from global_qad_ci. Any question? Please contact yangyamei@xiaomi.com"
RD_TEST_INTRODUCTION = "此为手动触发monkey测试的测试结果, 有问题请联系{tester}@xiaomi.com\nThis is a test result from test triggered by manual. any question? Please contact {tester}@xiaomi.com"


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
