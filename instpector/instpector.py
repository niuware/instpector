import requests
from .apis.instagram import Authenticate, Followers, Following, Profile, Timeline
from .apis.exceptions import AuthenticateFailException, AuthenticateRevokeException

class Instpector:
    def __init__(self, app_info=None):
        self._auth = None
        self._app_info = app_info
        self._browser_session = requests.session()

    def __del__(self):
        if self._browser_session:
            self._browser_session.close()

    def setup_app(self, app_info):
        self._app_info = app_info

    def login(self, user, password):
        self._auth = Authenticate(self._browser_session, user, password, self._app_info)
        try:
            self._auth.login()
            return True
        except AuthenticateFailException as auth_exception:
            print(f"AuthenticateFailException: {auth_exception}")
            return False

    def logout(self):
        if not self._auth:
            print("No active session found.")
            return
        try:
            self._auth.logout()
        except AuthenticateRevokeException as auth_exception:
            print(f"AuthenticateRevokeException: {auth_exception}")

    def followers(self):
        return Followers(self._browser_session)

    def following(self):
        return Following(self._browser_session)

    def profile(self):
        return Profile(self._browser_session)

    def timeline(self):
        return Timeline(self._browser_session)
