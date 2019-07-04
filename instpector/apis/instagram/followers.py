from .base_follow_edge import BaseFollowEdge
from .parser import Parser


class Followers(BaseFollowEdge):

    def __init__(self, browser_session):
        super().__init__("c76146de99bb02f6415203be841dd25a", browser_session)

    def get_all_for(self, user_id):
        return super()._get_all(user_id, Parser.followers_page_info, Parser.followers)
