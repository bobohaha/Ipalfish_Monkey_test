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
                TEST_STAGE_FIELD: TEST_STAGE_MONKEY,
                REPRODUCTIVITY_FIELD: REPRODUCTIVITY_SOMETIMES,
                LABELS_FIELD: [LABEL_GLOBAL_DEFAULT, LABEL_GLOBAL_DEV_CI]
            }
            pass

        def set_component(self, component):
            self.jira_content[COMPONENTS_FIELD] = component

        @property
        def component(self):
            return self.jira_content[COMPONENTS_FIELD]

        def set_summary(self, summary):
            self.jira_content[SUMMARY_FIELD] = summary

        @property
        def summary(self):
            return self.jira_content[SUMMARY_FIELD]

        def set_description(self, description):
            self.jira_content[DESCRIPTION_FIELD] = description

        @property
        def description(self):
            return self.jira_content[DESCRIPTION_FIELD]

        def set_device_name(self, device_name_list):
            self.jira_content[DEVICE_NAME] = device_name_list

        @property
        def device_name(self):
            return self.jira_content[DEVICE_NAME]

        def set_assignee(self, assignee):
            self.jira_content[ASSIGNEE_FIELD] = assignee

        @property
        def assignee(self):
            return self.jira_content[ASSIGNEE_FIELD]

        def set_reproductivity(self, reproductivity):
            self.jira_content[REPRODUCTIVITY_FIELD] = reproductivity,

        @property
        def reproductivity(self):
            return self.jira_content[REPRODUCTIVITY_FIELD]

        def set_affects_versions(self, version_list):
            self.jira_content[AFFECTS_VERSIONS_FIELD] = version_list

        @property
        def affects_versions(self):
            return self.jira_content[AFFECTS_VERSIONS_FIELD]

        def set_android_versions(self, android_version_list):
            self.jira_content[ANDROID_VERSION_FIELD] = android_version_list

        @property
        def android_versions(self):
            return self.jira_content[ANDROID_VERSION_FIELD]
