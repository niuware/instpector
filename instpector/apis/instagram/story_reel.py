import json
from ..exceptions import ParseDataException
from .base_api import BaseApi
from .parser import Parser


class StoryReel(BaseApi):

    def __init__(self, browser_session):
        super().__init__("https://www.instagram.com", browser_session)

    def of_user(self, user_id):
        params = {
            "query_hash": "cda12de4f7fd3719c0569ce03589f4c4",
            "variables": json.dumps({
                "reel_ids": [user_id],
                "tag_names": [],
                "location_ids": [],
                "highlight_reel_ids": [],
                "precomposed_overlay": False,
                "show_story_viewer_list": True,
                "story_viewer_fetch_count": 50,
                "story_viewer_cursor": "",
                "stories_video_dash_manifest": False
            })
        }
        try:
            data = super().get(f"/graphql/query/", params=params, headers={
                "DNT": "1"
            })
            if data:
                return Parser.story_reel(data)
        except ParseDataException:
            print(f"Invalid story reel data for user id {user_id}")
        return None

    def download(self, story_item, low_quality=False):
        self._download_resources(story_item, "display_resources", "jpg", low_quality)
        self._download_resources(story_item, "video_resources", "mp4", low_quality)

    def _download_resources(self, story_item, name, extension, low_quality):
        try:
            resources = getattr(story_item, name)
        except AttributeError:
            return
        if resources:
            quality = (len(resources) - 1) if not low_quality else 0
            super().download_file(resources[quality].get("src"), f"{story_item.id}.{extension}")
