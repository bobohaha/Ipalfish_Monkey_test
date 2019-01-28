from proxy.utils.JIRAUtil import JIRAUtil
from proxy.monkeyTest.MonkeyJiraParam import *


class MonkeyJiraUtil(JIRAUtil):
    def __init__(self):
        JIRAUtil.__init__(self, USERNAME, PASSWORD)
        self.jira_content = MonkeyJiraUtil.JiraContent()
        pass

    def create_monkey_task(self):
        self.set_jira_content(self.jira_content.jira_content)
        return self.create_or_edit_issue()

    class JiraContent:
        def __init__(self):
            self.jira_content = {
                PROJECT_FIELD: PROJECT_MONKEY,
                ISSUE_TYPE_FIELD: ISSUE_TYPE_MONKEY,
                PRIORITY_FIELD: PRIORITY_MONKEY,
                BUG_TYPE_FIELD: BUG_TYPE_MONKEY,
                REPRODUCTIVITY_FIELD: REPRODUCTIVITY_MONKEY,
                TEST_STAGE_FIELD: TEST_STAGE_MONKEY,
                LABELS_FIELD: [LABEL_GLOBAL_DEFAULT, LABEL_GLOBAL_DEV_CI]
            }
            pass

        def set_component(self, component):
            self.jira_content[COMPONENTS_FIELD] = component

        def set_summary(self, summary):
            self.jira_content[SUMMARY_FIELD] = summary

        def set_description(self, description):
            self.jira_content[DESCRIPTION_FIELD] = description

        def set_device_name(self, device_name_list):
            self.jira_content[DEVICE_NAME] = device_name_list

        def set_assignee(self, assignee):
            self.jira_content[ASSIGNEE_FIELD] = assignee

        def set_affects_versions(self, version_list):
            self.jira_content[AFFECTS_VERSIONS_FIELD] = version_list

        def set_android_versions(self, android_version_list):
            self.jira_content[ANDROID_VERSION_FIELD] = android_version_list
