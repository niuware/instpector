from .base_graph_ql import BaseGraphQL
from .parser import Parser


class Story(BaseGraphQL):

    def viewers_for(self, item_id):
        variables = {
            "item_id": item_id,
            "story_viewer_fetch_count": 50,
            "story_viewer_cursor": "0"
        }
        return self._loop("42c6ec100f5e57a1fe09be16cd3a7021",
                          variables=variables,
                          page_info_parser="edge_story_media_viewers",
                          page_info_parser_path="media",
                          page_info_next_cursor="story_viewer_cursor",
                          data_parser=Parser.story)
