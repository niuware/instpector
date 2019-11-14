from .base_follow import BaseFollow
from .parser import Parser


class Following(BaseFollow):

    def __init__(self, instance):
        super().__init__("d04b0a864b4b54837c0d870b0e77e076", instance)

    def of_user(self, user_id):
        return super()._get_all(user_id, "edge_follow", Parser.following)
