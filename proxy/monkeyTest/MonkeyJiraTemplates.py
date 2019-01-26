# coding=utf-8
from string import Template


BUG_DETAILS = '''
测试包名: $package
Bug类型: $bug_type
设备名称: $device_names
rom版本: $rom_versions
-------------------------------------------------------------
$bug_details
_____________________________________________________________
有任何问题，请联系yangyamei@xiaomi.com
'''


class JiraMonkeySummaryTemplate(Template):
    def __init__(self):
        Template.__init__(self, '[ $bug_type ] $bug_summary')
        pass


class JiraMonkeyDescriptionTemplate(Template):
    def __init__(self):
        Template.__init__(self, BUG_DETAILS)


class JiraCommentTemplate(Template):
    def __init__(self):
        Template.__init__(self, BUG_DETAILS)


# if __name__ == "__main__":
#     jira_summary = JiraMonkeyDescriptionTemplate()
#     a = jira_summary.substitute(package='testpkg',
#                                 bug_type="bug",
#                                 device_names="test_dev",
#                                 rom_versions="1.0",
#                                 bug_details='test something')
#     print a
