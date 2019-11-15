from .like_graph_ql import LikeGraphQL
from .parser import Parser


class Timeline(LikeGraphQL):

    def __init__(self, instance):
        super().__init__(instance, "/web/likes/{id}/{action}/")

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
