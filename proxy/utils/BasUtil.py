import os
try:
    import requests
except ImportError:
    os.system("pip install requests")
    import requests
from requests.sessions import HTTPAdapter


class BasUtil:
    BAS_HOST = "http://preview.bas.pt.miui.com"
    ANALYSIS_API = "/analysis/uploadAndGetSimpleInfo.do"

    def __init__(self, timeout=30, max_retries=3):
        self._max_retries = max_retries
        self._timeout = timeout

        self._init_session_header()
        self._init_session()
        self._init_url()

        self.files = {}
        self.body = {}
        pass

    def _init_session_header(self):
        self.session_header = {"backdoor": "reboot_miui_global"}

    def _init_session(self):
        self.session = requests.Session()
        self.session.headers.update(self.session_header)
        self.session.mount("http://", HTTPAdapter(max_retries=self._max_retries))
        self.session.mount("https://", HTTPAdapter(max_retries=self._max_retries))

    def _init_url(self):
        self.bas_url = "%s%s" % (self.BAS_HOST, self.ANALYSIS_API)

    def generate_bas_analysis_request_body(self, package=None):
        if package is None:
            self.body = None
        else:
            self.body['pkg'] = package

    def add_files_to_requests(self, file_names):
        if not isinstance(file_names, list):
            self.files["file"] = open(file_names, "rb")
        elif len(file_names) == 1:
            self.files["file"] = open(file_names[0], "rb")
        else:
            file_list = []
            for file_name in file_names:
                file_list.append(('file', open(file_name, "rb")))
            self.files = file_list

    def analysis(self, file_names, package=None):
        self.add_files_to_requests(file_names)
        self.generate_bas_analysis_request_body(package)
        response = self.session.post(self.bas_url, data=self.body, files=self.files)
        if response.status_code is requests.codes.ok:
            try:
                return response.json()['data']['bugs']
            except (ValueError, KeyError):
                print "analysis error", response.status_code, response.content
                return {}
        else:
            print "analysis error", response.status_code, response.content
            return {}


# if __name__ == "__main__":
#     upload_file_name = "/Users/may/Downloads/riva_8.12.21_261152.zip"
#     # ["/Users/may/Downloads/riva_8.12.21_261152.zip", "/Users/may/Downloads/riva_8.12.21_274956.zip"]
#     bas = BasUtil()
#     result = bas.analysis(upload_file_name, "com.mi.android.globallauncher")
#     print result['data']['bugs']
