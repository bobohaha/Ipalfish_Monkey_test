# coding=utf-8
from proxy.utils.JIRAParam import *
import proxy.monkeyTest.MonkeyJiraParam
from proxy.utils.JIRAUtil import JIRAUtil

if __name__ == '__main__':
    sanity_check_username = proxy.monkeyTest.MonkeyJiraParam.USERNAME
    sanity_check_password = proxy.monkeyTest.MonkeyJiraParam.PASSWORD
    issue_owner = proxy.monkeyTest.MonkeyJiraParam.ISSUE_DEFAULT_OWNER

    jira_contents = {
        PROJECT_FIELD: proxy.monkeyTest.MonkeyJiraParam.PROJECT_MONKEY,
        ISSUE_TYPE_FIELD: proxy.monkeyTest.MonkeyJiraParam.ISSUE_TYPE_MONKEY,
        COMPONENTS_FIELD: COMPONENT_POCO_LAUNCHER,
        SUMMARY_FIELD: "[Global_Dev_CI]",
        DESCRIPTION_FIELD: "Global Dev CI",
        DEVICE_NAME: ["beryllium_global", "whyred_global"],
        PRIORITY_FIELD: proxy.monkeyTest.MonkeyJiraParam.PRIORITY_MONKEY,
        ASSIGNEE_FIELD: issue_owner,
        AFFECTS_VERSIONS_FIELD: ["9.1.3"],
        ANDROID_VERSION_FIELD: ["9.0", "8.1"],
        BUG_TYPE_FIELD: BUG_TYPE_STABILITY,
        REPRODUCTIVITY_FIELD: REPRODUCTIVITY_EVERY_TIME,
        TEST_STAGE_FIELD: TEST_STAGE_DEVELOPMENT,
        LABELS_FIELD: [LABEL_GLOBAL_DEFAULT, "Global_Dev_Ci"]
    }

    print jira_contents is None

    jira_util = JIRAUtil(sanity_check_username, sanity_check_password)
    # jira_util.set_jira_content(jira_content=jira_contents)
    # print jira_util.get_jira_common_data()
    # # jira_util.set_jira_summary("Auto Test Modified")
    # # print jira_util.get_jira_common_data()
    # rst_site = jira_util.create_or_edit_issue()
    # jira_util.add_attachment("MIUI-1514761", "/Users/may/Downloads/riva_8.12.21_261152.zip")
    # jira_util.add_watchers("MIUI-1514761", "")
    jira_util.add_comment("MIUI-1514761", "test_comment")
