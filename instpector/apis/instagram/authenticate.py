import json
from ..http_request import HttpRequest, HttpRequestMode
from ..exceptions import AuthenticateFailException, AuthenticateRevokeException
from .utilities import get_ajax_id, get_consumer_lib_path, get_app_id


class Authenticate(HttpRequest):

    def __init__(self, browser_session, user, password, app_info=None):
        self._user = user
        self._password = password
        self._app_info = app_info
        self._auth_headers = {}
        self._auth_cookies = {}
        super().__init__("https://www.instagram.com", browser_session)

    def login(self):
        self._login_prepare()
        if self._auth_headers:
            self._login_execute()
            return
        raise AuthenticateFailException("Login prepare unsuccessful")

    def logout(self):
        if not self._auth_cookies or not self._auth_cookies.get("csrftoken"):
            raise AuthenticateRevokeException("No session information found.")
        headers = {
            "Referer": f"https://www.instagram.com/{self._user}",
            "Upgrade-Insecure-Requests": "1",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {
            "csrfmiddlewaretoken": self._auth_cookies.get("csrftoken")
        }
        response = self.post("/accounts/logout",
                             mode=HttpRequestMode.FORM,
                             data=data,
                             headers=headers)
        if response.status_code != 301:
            raise AuthenticateRevokeException("Logout unsuccessful")
        print("Logged out")

    def _lookup_headers(self):
        html = self.get("/", stream=True)
        ajax_id = get_ajax_id(html.text)
        js_lib_path = get_consumer_lib_path(html.iter_lines(decode_unicode=True))
        js_lib = self.get(js_lib_path)
        app_id = get_app_id(js_lib.text)
        return app_id, ajax_id

    def _login_prepare(self):
        headers = {
            "Upgrade-Insecure-Requests": "1"
        }
        response = self.get("/accounts/login/?source=auth_switcher",
                            mode=HttpRequestMode.FORM,
                            headers=headers,
                            redirects=True)
        self._auth_headers = response.cookies.get_dict(".instagram.com")
        if not self._app_info:
            app_id, ajax_id = self._lookup_headers()
            self._app_info = {
                "ig_app_id": app_id,
                "ig_ajax_id": ajax_id
            }

    def _login_execute(self):
        data = {
            "username": self._user,
            "password": self._password,
            "queryParams": "{\"source\":\"auth_switcher\"}",
            "optIntoOneTap": "true"
        }
        headers = {
            "Referer": "https://www.instagram.com/accounts/login/?source=auth_switcher",
            "X-CSRFToken": self._auth_headers.get("csrftoken"),
            "X-Instagram-AJAX": self._app_info.get("ig_ajax_id", ""),
            "X-IG-App-ID": self._app_info.get("ig_app_id", ""),
            "Content-Type": "application/x-www-form-urlencoded",
        }
        response = self.post("/accounts/login/ajax/",
                             data=data,
                             headers=headers,
                             redirects=True)
        try:
            data = json.loads(response.text)
            self._auth_cookies = response.cookies.get_dict(".instagram.com")
            return self._parse_login(data)
        except json.decoder.JSONDecodeError:
            raise AuthenticateFailException("Unexpected login response.")

    def _parse_login(self, data):
        if data and data.get("authenticated"):
            user_id = data.get("userId")
            print(f"Logged in as {self._user} (Id: {user_id})")
            return
        raise AuthenticateFailException("Login unsuccessful")
