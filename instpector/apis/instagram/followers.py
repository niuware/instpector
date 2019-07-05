from .base_follow import BaseFollow
from .parser import Parser


class Followers(BaseFollow):

    def __init__(self, browser_session):
        super().__init__("c76146de99bb02f6415203be841dd25a", browser_session)

    def get_all_for(self, user_id):
        return super()._get_all(user_id, "edge_followed_by", Parser.followers)
