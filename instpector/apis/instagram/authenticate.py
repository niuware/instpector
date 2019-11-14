import json
from ..http_request import HttpRequest, HttpRequestMode
from ..exceptions import AuthenticateFailException, AuthenticateRevokeException
from .utilities import get_ajax_id, get_consumer_lib_path, get_app_id


class Authenticate(HttpRequest):

    def __init__(self, instance, user, password, two_factor_code):
        self._user = user
        self._password = password
        self._two_factor_code = two_factor_code
        self._app_info = {}
        self._auth_headers = {}
        self._auth_cookies = {}
        super().__init__("https://www.instagram.com", instance)

    def login(self):
        self._login_prepare()
        if self._auth_headers:
            self._login_execute()
            return
        raise AuthenticateFailException("Login prepare unsuccessful")

    def logout(self):
        if not self.is_logged_in():
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
        if not response or response.status_code != 301:
            raise AuthenticateRevokeException("Logout unsuccessful")
        print("Logged out")

    def is_logged_in(self):
        return self._auth_cookies and self._auth_cookies.get("csrftoken")

    def get_auth_headers(self):
        return {
            "X-CSRFToken": self._auth_cookies.get("csrftoken", ""),
            "X-Instagram-AJAX": self._app_info.get("ig_ajax_id", ""),
            "X-IG-App-ID": self._app_info.get("ig_app_id", "")
        }

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
        if not response:
            return
        self._auth_headers = response.cookies.get_dict(".instagram.com")
        app_id, ajax_id = self._lookup_headers()
        self._app_info['ig_app_id'] = app_id
        self._app_info['ig_ajax_id'] = ajax_id

    def _login_execute(self):
        data = {
            "username": self._user,
            "password": self._password,
            "queryParams": "{\"source\":\"auth_switcher\"}",
            "optIntoOneTap": "true"
        }
        self._attempt_login("/accounts/login/ajax/", data, self._two_factor_code is not None)

    def _login_two_factor(self, identifier):
        data = {
            "username": self._user,
            "verificationCode": self._two_factor_code,
            "queryParams": "{\"source\":\"auth_switcher\", \"next\":\"/\"}",
            "identifier": identifier
        }
        self._attempt_login("/accounts/login/ajax/two_factor/", data)

    def _attempt_login(self, url, data, use_2fa=False):
        auth_headers = self.get_auth_headers()
        auth_headers['X-CSRFToken'] = self._auth_headers.get("csrftoken")
        post_headers = {
            "Referer": "https://www.instagram.com/accounts/login/?source=auth_switcher",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        headers = {**post_headers, **auth_headers}
        response = self.post(url,
                             data=data,
                             headers=headers,
                             redirects=True)
        try:
            data = json.loads(response.text)
            self._auth_cookies = response.cookies.get_dict(".instagram.com")
            self._parse_login(data, use_2fa)
        except (json.decoder.JSONDecodeError, AttributeError):
            raise AuthenticateFailException("Unexpected login response.")

    def _parse_login(self, data, use_2fa):
        if data:
            if data.get("authenticated"):
                user_id = data.get("userId")
                print(f"Logged in as {self._user} (Id: {user_id})")
                return
            if use_2fa and data.get("two_factor_required")\
               and data.get("two_factor_info"):
                self._login_two_factor(data.get("two_factor_info").get("two_factor_identifier"))
                return
        raise AuthenticateFailException("Login unsuccessful")
