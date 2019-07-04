from .base_follow_edge import BaseFollowEdge
from .parser import Parser


class Following(BaseFollowEdge):

    def __init__(self, browser_session):
        super().__init__("d04b0a864b4b54837c0d870b0e77e076", browser_session)

    def get_all_for(self, user_id):
        return super()._get_all(user_id, Parser.following_page_info, Parser.following)
