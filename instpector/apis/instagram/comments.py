from .like_graph_ql import LikeGraphQL
from .parser import Parser
from .definitions import TComment


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

    def add(self, timeline_post, text, parent_comment=None):
        post_id = getattr(timeline_post, "id", None)
        if post_id is None:
            return False
        comment_id = getattr(parent_comment, "id") if parent_comment else ""
        data = {
            "comment_text": text,
            "replied_to_comment_id": comment_id,
        }
        response = self.post("/web/comments/{id}/add/".format(id=post_id),
                             data=data, use_auth=True,
                             headers={
                                 "Content-Type": "application/x-www-form-urlencoded"
                             })
        if response and response.get("status") == "ok":
            owner = response.get("from") or {}
            thread_count = 0 if comment_id == "" else None
            return TComment(
                id=response.get("id", ""),
                text=response.get("text", ""),
                timestamp=response.get("created_time"),
                username=owner.get("username", ""),
                viewer_has_liked=False,
                liked_count=0,
                thread_count=thread_count
            )
        return None

    def remove(self, timeline_post, comment):
        post_id = getattr(timeline_post, "id", None)
        if post_id is None:
            return False
        comment_id = getattr(comment, "id", None)
        if comment_id is None:
            return False
        url = "/web/comments/{id}/delete/{comment_id}/"
        return self.quick_post(url.format(id=post_id, comment_id=comment_id))
