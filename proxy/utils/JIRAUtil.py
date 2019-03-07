# coding=utf-8
import traceback
import requests
import base64
import json

import JIRAParam


class JIRAUtil:
    _jira_content = {}
    _jira_data = {JIRAParam.JIRA_UPDATE: {},
                  JIRAParam.JIRA_FIELDS: {}}

    def __init__(self, user_name, user_password):
        self._jira_session = JIRAUtil.JiraSession(user_name, user_password)
        pass

    def set_jira_content(self, jira_content):
        self._jira_content = jira_content
        self.set_jira_project()
        self.set_jira_issue_type()
        self.set_jira_summary()
        self.set_jira_components()
        self.set_jira_priority()
        self.set_jira_bug_type()
        self.set_jira_reproductivity()
        self.set_jira_assignee()
        self.set_jira_affects_version()
        self.set_jira_android_version()
        self.set_jira_model_tag()
        self.set_jira_test_stage()
        self.set_jira_description()
        self.set_jira_label()
        pass

    def get_jira_common_data(self):
        return self._jira_data

    def set_jira_project(self, project=None):
        if project:
            self._jira_data[JIRAParam.JIRA_FIELDS][JIRAParam.PROJECT_FIELD] = {'key': project}
        elif JIRAParam.PROJECT_FIELD in self._jira_content.keys():
            self.set_jira_project(self._jira_content[JIRAParam.PROJECT_FIELD])
        pass

    def set_jira_issue_type(self, issue_type=None):
        if issue_type:
            self._jira_data[JIRAParam.JIRA_FIELDS][JIRAParam.ISSUE_TYPE_FIELD] = {
                'name': issue_type}
        elif JIRAParam.ISSUE_TYPE_FIELD in self._jira_content.keys():
            self.set_jira_issue_type(self._jira_content[JIRAParam.ISSUE_TYPE_FIELD])
        pass

    def set_jira_summary(self, summary=None):
        if summary is not None:
            self._jira_data[JIRAParam.JIRA_FIELDS][JIRAParam.SUMMARY_FIELD] = summary
        elif JIRAParam.SUMMARY_FIELD in self._jira_content.keys():
            self.set_jira_summary(self._jira_content[JIRAParam.SUMMARY_FIELD])
        pass

    def set_jira_components(self, components=None):
        if components is not None:
            self._jira_data[JIRAParam.JIRA_FIELDS][JIRAParam.COMPONENTS_FIELD] = [
                {'name': components}]
        elif JIRAParam.COMPONENTS_FIELD in self._jira_content.keys():
            self.set_jira_components(self._jira_content[JIRAParam.COMPONENTS_FIELD])
        pass

    def set_jira_priority(self, priority=None):
        if priority:
            self._jira_data[JIRAParam.JIRA_FIELDS][JIRAParam.PRIORITY_FIELD] = {'name': priority}
        elif JIRAParam.PRIORITY_FIELD in self._jira_content.keys():
            self.set_jira_priority(self._jira_content[JIRAParam.PRIORITY_FIELD])
        else:
            self.set_jira_priority(JIRAParam.PRIORITY_TRIVIAL)
        pass

    def set_jira_bug_type(self, bug_type=None):
        if bug_type:
            self._jira_data[JIRAParam.JIRA_FIELDS][JIRAParam.BUG_TYPE_FIELD] = {'value': bug_type}
        elif JIRAParam.BUG_TYPE_FIELD in self._jira_content.keys():
            self.set_jira_bug_type(self._jira_content[JIRAParam.BUG_TYPE_FIELD])
        pass

    def set_jira_reproductivity(self, reproductivity=None):
        if reproductivity:
            self._jira_data[JIRAParam.JIRA_FIELDS][JIRAParam.REPRODUCTIVITY_FIELD] = {
                'value': reproductivity}
        elif JIRAParam.REPRODUCTIVITY_FIELD in self._jira_content.keys():
            self.set_jira_reproductivity(self._jira_content[JIRAParam.REPRODUCTIVITY_FIELD])
        pass

    def set_jira_assignee(self, assignee=None):
        if assignee:
            self._jira_data[JIRAParam.JIRA_FIELDS][JIRAParam.ASSIGNEE_FIELD] = {'name': assignee}
        elif JIRAParam.ASSIGNEE_FIELD in self._jira_content.keys():
            self.set_jira_assignee(self._jira_content[JIRAParam.ASSIGNEE_FIELD])
        # else:
        #     raise Exception("Please give the assignee")
        pass

    def set_jira_affects_version(self, affects_version=None):
        if affects_version:
            self._jira_data[JIRAParam.JIRA_UPDATE][JIRAParam.AFFECTS_VERSIONS_FIELD] = list()
            if not isinstance(affects_version, list):
                self._jira_data[JIRAParam.JIRA_UPDATE][JIRAParam.AFFECTS_VERSIONS_FIELD] = [{
                    'add': {'name': affects_version}
                }]
            else:
                for version in affects_version:
                    self._jira_data[JIRAParam.JIRA_UPDATE][JIRAParam.AFFECTS_VERSIONS_FIELD].append({
                        'add': {'name': version}
                    })
        elif JIRAParam.AFFECTS_VERSIONS_FIELD in self._jira_content.keys():
            self.set_jira_affects_version(self._jira_content[JIRAParam.AFFECTS_VERSIONS_FIELD])
        pass

    def set_jira_android_version(self, android_version=None):
        if android_version:
            self._jira_data[JIRAParam.JIRA_UPDATE][JIRAParam.ANDROID_VERSION_FIELD] = list()
            if not isinstance(android_version, list):
                self._jira_data[JIRAParam.JIRA_UPDATE][JIRAParam.ANDROID_VERSION_FIELD] = [{
                    'add': {'value': android_version}
                }]
            else:
                for version in android_version:
                    self._jira_data[JIRAParam.JIRA_UPDATE][JIRAParam.ANDROID_VERSION_FIELD].append({
                        'add': {'value': version}
                    })
        elif JIRAParam.ANDROID_VERSION_FIELD in self._jira_content.keys():
            self.set_jira_android_version(self._jira_content[JIRAParam.ANDROID_VERSION_FIELD])
        pass

    def set_jira_model_tag(self, model_tags=None):
        if model_tags:
            self._jira_data[JIRAParam.JIRA_UPDATE][JIRAParam.MODEL_TAG_FIELD] = list()
            if not isinstance(model_tags, list):
                self._jira_data[JIRAParam.JIRA_UPDATE][JIRAParam.MODEL_TAG_FIELD] = [{
                    'add': {'value': model_tags}
                }]
            else:
                for tag in model_tags:
                    self._jira_data[JIRAParam.JIRA_UPDATE][JIRAParam.MODEL_TAG_FIELD].append({
                        'add': {'value': tag}
                    })
        elif JIRAParam.DEVICE_NAME in self._jira_content.keys():
            if not isinstance(self._jira_content[JIRAParam.DEVICE_NAME], list):
                self.set_jira_model_tag(self.get_model_tag(self._jira_content[JIRAParam.DEVICE_NAME]))
            else:
                tags = list()
                for device in self._jira_content[JIRAParam.DEVICE_NAME]:
                    tags.append(self.get_model_tag(device))
                self.set_jira_model_tag(tags)
        else:
            self.set_jira_model_tag(JIRAParam.MODEL_TAG_ALL_DEVICES)
        pass

    @classmethod
    def get_model_tag(cls, device_name):
        model_tag = JIRAParam.get_miui_model(device_name)

        if model_tag is not None:
            return model_tag

        return JIRAParam.MODEL_TAG_ALL_DEVICES

    def set_jira_test_stage(self, test_stage=None):
        if test_stage:
            self._jira_data[JIRAParam.JIRA_FIELDS][JIRAParam.TEST_STAGE_FIELD] = {
                'value': test_stage}
        elif JIRAParam.TEST_STAGE_FIELD in self._jira_content.keys():
            self.set_jira_test_stage(self._jira_content[JIRAParam.TEST_STAGE_FIELD])
        pass

    def set_jira_description(self, description=None):
        if description:
            self._jira_data[JIRAParam.JIRA_FIELDS][JIRAParam.DESCRIPTION_FIELD] = description
        elif JIRAParam.DESCRIPTION_FIELD in self._jira_content.keys():
            self.set_jira_description(self._jira_content[JIRAParam.DESCRIPTION_FIELD])
        pass

    def set_jira_label(self, labels=None):
        if labels:
            self._jira_data[JIRAParam.JIRA_UPDATE][JIRAParam.LABELS_FIELD] = list()
            if not isinstance(labels, list):
                self._jira_data[JIRAParam.JIRA_UPDATE][JIRAParam.LABELS_FIELD] = [{
                    'add': labels
                }]
            else:
                for label in labels:
                    self._jira_data[JIRAParam.JIRA_UPDATE][JIRAParam.LABELS_FIELD].append({
                        'add': label
                    })
        elif JIRAParam.LABELS_FIELD in self._jira_content.keys():
            self.set_jira_label(self._jira_content[JIRAParam.LABELS_FIELD])
        pass

    #  Actually edit issue is not available
    def create_or_edit_issue(self, jira_content=None, jira_id_or_key=None):
        if jira_content is not None:
            self.set_jira_content(jira_content)

        issue_api = JIRAParam.JIRA_CREATE_ISSUE_API if jira_id_or_key is None \
            else JIRAParam.JIRA_EDIT_ISSUE_API.format(issueIdOrKey=jira_id_or_key)
        create_issue_url = '%s:%s%s' % (
            JIRAParam.JIRA_HOST, JIRAParam.JIRA_PORT, issue_api)
        try:
            self._jira_session.add_header('Accept', 'application/json')
            self._jira_session.add_header('Content-type', 'application/json')
            r = self._jira_session.post(_url=create_issue_url, _data=json.dumps(self._jira_data))
            print r, r.status_code, r.content
            if r.status_code >= 300 or r.status_code < 200:
                return r.json()
            else:
                return r.json()
        except Exception, why:
            print "create issue error", why
            print traceback.format_exc()

    @classmethod
    def get_jira_id(cls, result):
        jira_id = result.get('id')
        return jira_id

    @classmethod
    def get_jira_key(cls, result):
        jira_key = result.get('key')
        return jira_key

    @classmethod
    def get_jira_site(cls, jira_key):
        jira_site = JIRAParam.JIRA_ISSUE_LINK.format(issueIdOrKey=jira_key)
        return jira_site

    def add_attachment(self, jira_id_or_key, file_names):
        add_attachment_jira_url = '%s:%s%s' % (
            JIRAParam.JIRA_HOST, JIRAParam.JIRA_PORT, JIRAParam.JIRA_ADD_ATTACHMENT_API.format(issueIdOrKey=jira_id_or_key))
        try:
            self._jira_session.add_header('X-Atlassian-Token', 'no-check')
            files = dict()
            if not isinstance(file_names, list):
                files['file'] = open(file_names, "rb")
            elif len(file_names) == 1:
                files['file'] = open(file_names[0], "rb")
            else:
                file_list = []
                for file_name in file_names:
                    file_list.append(open(file_name, "rb"))
                files['file'] = file_list

            r = self._jira_session.post(_url=add_attachment_jira_url, files=files)
            print r, r.status_code, r.content
            return r.status_code == 200
        except Exception, why:
            print "add_attachment error: ", why
            print traceback.format_exc()

    def add_comment(self, jira_id_or_key, comment):
        add_comment_jira_url = '{}:{}{}'.format(JIRAParam.JIRA_HOST,
                                                JIRAParam.JIRA_PORT,
                                                JIRAParam.JIRA_ADD_COMMENT_API.format(issueIdOrKey=jira_id_or_key))
        try:
            self._jira_session.add_header('Accept', 'application/json')
            self._jira_session.add_header('Content-Type', 'application/json')
            post_data = {
                'body': comment
            }
            r = self._jira_session.post(_url=add_comment_jira_url, _json=post_data)
            print r, r.status_code, r.content
            return 200 <= r.status_code < 300
        except Exception, why:
            print "add_comment error", why
            print traceback.format_exc()

    def add_watchers(self, jira_id_or_key, watchers):
        add_watchers_jira_url = '{}:{}{}'.format(JIRAParam.JIRA_HOST,
                                                 JIRAParam.JIRA_PORT,
                                                 JIRAParam.JIRA_ADD_WATCHER_API.format(issueIdOrKey=jira_id_or_key))
        try:
            self._jira_session.add_header('Content-Type', 'application/json')
            post_data = json.dumps(watchers)
            r = self._jira_session.post(add_watchers_jira_url, _data=post_data)
            print r, r.status_code, r.content
            return r.status_code == 204
        except Exception, why:
            print "add_watchers error: ", why
            print traceback.format_exc()

    def is_can_reopen_issue(self, jira_id_or_key):
        get_transition_url = '{}:{}{}'.format(JIRAParam.JIRA_HOST,
                                              JIRAParam.JIRA_PORT,
                                              JIRAParam.JIRA_TRANSITION_API.format(issueIdOrKey=jira_id_or_key))
        try:
            self._jira_session.add_header('Accept', 'application/json')
            r = self._jira_session.get(get_transition_url)
            print r, r.status_code, r.content
            if r.status_code == 200:
                transitions = r.json()['transitions']
                for transition in transitions:
                    if transition['name'] == "Reopen Issue":
                        return True
        except Exception, why:
            print "is_can_reopen_issue error: ", why
            print traceback.format_exc()
        return False

    def change_issue_to_reopen(self, jira_id_or_key):
        get_transition_url = '{}:{}{}'.format(JIRAParam.JIRA_HOST,
                                              JIRAParam.JIRA_PORT,
                                              JIRAParam.JIRA_TRANSITION_API.format(issueIdOrKey=jira_id_or_key))
        try:
            self._jira_session.add_header('Content-Type', 'application/json')
            post_data = json.dumps({
                "transition": {
                    "id": "211"
                }
            })
            r = self._jira_session.post(get_transition_url, _data=post_data)
            print r, r.status_code, r.content
            return r.status_code == 204
        except Exception, why:
            print "change_issue_to_reopen error: ", why
            print traceback.format_exc()
        return False

    def open_jira_task(self, jira_content=None):
        self.set_jira_issue_type(JIRAParam.ISSUE_TYPE_TASK)
        result = self.create_or_edit_issue(jira_content=jira_content)
        return self.get_jira_site(result)

    def open_trivial_task(self, jira_content=None):
        self.set_jira_priority(JIRAParam.PRIORITY_TRIVIAL)
        return self.open_jira_task(jira_content=jira_content)

    def open_jira_task_with_files(self, file_names, jira_content=None):
        self.set_jira_issue_type(JIRAParam.ISSUE_TYPE_TASK)
        result = self.create_or_edit_issue(jira_content=jira_content)
        jira_id = self.get_jira_id(result)
        self.add_attachment(jira_id, file_names)
        return self.get_jira_site(result)

    def open_trivial_task_with_files(self, file_names, jira_content=None):
        self.set_jira_priority(JIRAParam.PRIORITY_TRIVIAL)
        return self.open_jira_task_with_files(file_names=file_names, jira_content=jira_content)

    class JiraSession:
        def __init__(self, auth_user_name, auth_user_pwd):
            self.session = requests.Session()
            self._jira_header = {}
            self._auth_user_name = auth_user_name
            self._auth_user_pwd = auth_user_pwd
            self._init_auth()

        def _init_auth(self):
            auth_str = base64.encodestring(
                '%s:%s' % (self._auth_user_name, self._auth_user_pwd)).replace('\n', '')
            self._jira_header["Authorization"] = "Basic %s" % auth_str

        def add_header(self, header_key, header_value):
            self._jira_header[header_key] = header_value

        def _update_header(self):
            self.session.headers.update(self._jira_header)

        def post(self, _url, _data=None, _json=None, **kwargs):
            self._update_header()
            return self.session.post(_url, _data, _json, **kwargs)

        def get(self, _url, **kwargs):
            self._update_header()
            return self.session.get(_url, **kwargs)
