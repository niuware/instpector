from .base_follow import BaseFollow
from .parser import Parser


class Following(BaseFollow):

    def __init__(self, browser_session):
        super().__init__("d04b0a864b4b54837c0d870b0e77e076", browser_session)

    def get_all_for(self, user_id):
        return super()._get_all(user_id, "edge_follow", Parser.following)
