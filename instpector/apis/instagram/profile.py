from ..base_api import BaseApi
from ..exceptions import ParseDataException
from .parser import Parser


class Profile(BaseApi):

    def __init__(self, browser_session):
        super().__init__("https://www.instagram.com", browser_session)

    def get_for(self, username):
        params = {
            "__a": 1
        }
        headers = {
            "DNT": "1"
        }
        try:
            data = super().get(f"/{username}/", params=params, headers=headers)
            if data:
                return Parser.profile(data)
        except ParseDataException:
            print(f"Invalid data for username {username}")
        return None
