from ..exceptions import ParseDataException
from .base_api import BaseApi
from .parser import Parser


class Profile(BaseApi):

    def __init__(self, instance):
        super().__init__("https://www.instagram.com", instance)

    def of_user(self, username):
        params = {
            "__a": 1
        }
        try:
            data = super().get(f"/{username}/", params=params, headers={
                "DNT": "1"
            })
            if data:
                return Parser.profile(data)
        except ParseDataException:
            print(f"Invalid data for username {username}")
        return None

    def activity(self):
        data = super().get("/accounts/activity/?__a=1&include_reel=true")
        if data:
            try:
                return Parser.activity(data)
            except ParseDataException:
                pass
        return None

    def _toggle_follow(self, user, action):
        tuser = user
        if isinstance(user, str):
            tuser = self.of_user(user)
        user_id = getattr(tuser, "id", "")
        if user_id:
            return super().quick_post(f"/web/friendships/{user_id}/{action}/")
        return False

    def follow(self, user):
        return self._toggle_follow(user, "follow")

    def unfollow(self, user):
        return self._toggle_follow(user, "unfollow")
