import json
from ..exceptions import ParseDataException, NoDataException
from .base_api import BaseApi
from .parser import Parser
from .definitions import TPageInfo


class BaseGraphQL(BaseApi):
    DEFAULT_EDGE_COUNT = 12

    def __init__(self, instance):
        super().__init__("https://www.instagram.com", instance)

    def _loop(self, query_hash, variables, **parser_callbacks):
        page_info = TPageInfo(end_cursor=None, has_next_page=True)
        while True:
            if not page_info.has_next_page:
                return
            next_cursor_name = parser_callbacks.get("page_info_next_cursor")
            data = self._get_partial_data(query_hash, variables, page_info.end_cursor,
                                          next_cursor_name)
            if data:
                page_info = Parser.page_info(data, parser_callbacks.get("page_info_parser"),
                                             parser_callbacks.get("page_info_parser_path"))
                try:
                    for result in parser_callbacks.get("data_parser")(data):
                        yield result
                except NoDataException:
                    return

    def _get_partial_data(self, query_hash, variables, end_cursor, cursor_name):
        cursor_name = cursor_name or "after"
        cursor = end_cursor or ""
        if cursor_name != "after" and not cursor:
            cursor = "0"
        cursor_param = {
            cursor_name: cursor
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
