from .base_graph_ql import BaseGraphQL
from .parser import Parser


class Timeline(BaseGraphQL):

    def get_all_for(self, user_id):
        variables = {
            "id": user_id,
            "first": self.DEFAULT_EDGE_COUNT
        }
        return self._loop("f2405b236d85e8296cf30347c9f08c2a",
                          variables=variables,
                          page_info_parser="edge_owner_to_timeline_media",
                          data_parser=Parser.timeline)
