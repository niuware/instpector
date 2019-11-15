from .like_graph_ql import LikeGraphQL
from .parser import Parser


class Comments(LikeGraphQL):

    def __init__(self, instance):
        super().__init__(instance, "/web/comments/{action}/{id}/")

    def of_post(self, timeline_post):
        shortcode = getattr(timeline_post, "shortcode", None)
        if shortcode is None:
            return []
        variables = {
            "shortcode": shortcode,
            "first": self.DEFAULT_EDGE_COUNT
        }
        return self._loop("97b41c52301f77ce508f55e66d17620e",
                          variables=variables,
                          page_info_parser="edge_media_to_parent_comment",
                          page_info_parser_path="shortcode_media",
                          data_parser=Parser.parent_comments)

    def of_comment(self, comment):
        comment_id = getattr(comment, "id", None)
        if comment_id is None:
            return []
        variables = {
            "comment_id": comment_id,
            "first": 6
        }
        return self._loop("51fdd02b67508306ad4484ff574a0b62",
                          variables=variables,
                          page_info_parser="edge_threaded_comments",
                          page_info_parser_path="comment",
                          data_parser=Parser.threaded_comments)
