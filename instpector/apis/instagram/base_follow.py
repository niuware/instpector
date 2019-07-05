from .base_graph_ql import BaseGraphQL


class BaseFollow(BaseGraphQL):

    def __init__(self, query_hash, browser_session):
        self._query_hash = query_hash
        super().__init__(browser_session)

    def _get_all(self, user_id, page_info_parser, parse_cb):
        variables = {
            "id": user_id,
            "include_reel": True,
            "fetch_mutual": False,
            "first": self.DEFAULT_EDGE_COUNT
        }
        return self._loop(self._query_hash,
                          variables=variables,
                          page_info_parser=page_info_parser,
                          data_parser=parse_cb)
