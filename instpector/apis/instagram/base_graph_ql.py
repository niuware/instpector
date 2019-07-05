import json
from ..base_api import BaseApi
from ..exceptions import ParseDataException
from .parser import Parser
from .definitions import TPageInfo


class BaseGraphQL(BaseApi):
    DEFAULT_EDGE_COUNT = 12

    def __init__(self, browser_session):
        super().__init__("https://www.instagram.com", browser_session)

    def _loop(self, query_hash, variables, **parser_callbacks):
        page_info = TPageInfo(end_cursor=None, has_next_page=True)
        while True:
            if not page_info.has_next_page:
                return
            data = self._get_partial_data(query_hash, variables, page_info.end_cursor)
            if data:
                page_info = Parser.page_info(data, parser_callbacks.get("page_info_parser"))
                for result in parser_callbacks.get("data_parser")(data):
                    yield result

    def _get_partial_data(self, query_hash, variables, end_cursor):
        cursor = end_cursor or ""
        cursor_param = {
            "after": cursor
        }
        post_variables = json.dumps({**variables, **cursor_param})
        params = {
            "query_hash": query_hash,
            "variables": post_variables
        }
        try:
            return super().get("/graphql/query/", params=params)
        except ParseDataException:
            print(f"Invalid data for query {query_hash}")
        return None
