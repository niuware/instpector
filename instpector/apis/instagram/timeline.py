from .base_graph_ql import BaseGraphQL
from .parser import Parser


class Timeline(BaseGraphQL):

    def of_user(self, user_id):
        variables = {
            "id": user_id,
            "first": self.DEFAULT_EDGE_COUNT
        }
        return self._loop("f2405b236d85e8296cf30347c9f08c2a",
                          variables=variables,
                          page_info_parser="edge_owner_to_timeline_media",
                          data_parser=Parser.timeline)

    def download(self, timeline_post, only_image=False, low_quality=False):
        super()._download_resources_list(timeline_post, "display_resources", "jpg", low_quality)
        if not only_image:
            if timeline_post.video_url:
                file_name = f"{timeline_post.owner}_{timeline_post.id}.mp4"
                super().download_file(timeline_post.video_url, file_name)

    def _toggle_like(self, timeline_post, action):
        endpoint = 'like' if action == 'like' else 'unlike'
        post_id = getattr(timeline_post, "id", None)
        if post_id is None:
            return False
        response = self.post("/web/likes/" + post_id + "/" + endpoint + "/",
                             use_auth=True,
                             headers={
                                 "Content-Type": "application/x-www-form-urlencoded"
                             })
        if response and response.get("status") == "ok":
            return True
        return False

    def unlike(self, timeline_post):
        return self._toggle_like(timeline_post, 'unlike')

    def like(self, timeline_post):
        return self._toggle_like(timeline_post, 'like')
