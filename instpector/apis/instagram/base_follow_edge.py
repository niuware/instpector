import json
from ..http_request import HttpRequest
from .definitions import TPageInfo

class BaseFollowEdge(HttpRequest):
    DEFAULT_EDGE_COUNT = 12

    def __init__(self, query_hash, browser_session):
        self._query_hash = query_hash
        super().__init__("https://www.instagram.com", browser_session)

    def _get_all(self, user_id, parse_page_info_cb, parse_cb):
        page_info = TPageInfo(end_cursor=None, has_next_page=True)
        while True:
            if not page_info.has_next_page:
                return
            data = self._get_partial_data(user_id, page_info.end_cursor)
            if data:
                page_info = parse_page_info_cb(data)
                for user in parse_cb(data):
                    yield user

    def _get_partial_data(self, user_id, end_cursor):
        cursor = end_cursor or ""
        params = {
            "query_hash": self._query_hash,
            "variables": (
                f"{{\"id\":\"{user_id}\",\"include_reel\":true,"
                f"\"fetch_mutual\":false,\"first\":{self.DEFAULT_EDGE_COUNT}"
                f",\"after\":\"{cursor}\"}}"
            )
        }
        response = self.get("/graphql/query/", params=params)
        if response.status_code == 200:
            try:
                return json.loads(response.text)
            except json.decoder.JSONDecodeError:
                print(f"Invalid data for query_hash {self._query_hash} and user_id {user_id}")
        return None
