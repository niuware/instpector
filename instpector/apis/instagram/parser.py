from .definitions import TUser, TPageInfo, TProfile, TTimelinePost, TStoryReelItem, TStoryViewer


class Parser:

    @staticmethod
    def followers(data):
        return Parser._follow_edge(data, "edge_followed_by")

    @staticmethod
    def following(data):
        return Parser._follow_edge(data, "edge_follow")

    @staticmethod
    def profile(data):
        user_id = ""
        username = ""
        biography = ""
        followers_count = 0
        following_count = 0
        is_private = False
        try:
            user = data["graphql"]["user"]
            user_id = user["id"]
            username = user["username"]
            biography = user["biography"]
            followers_count = user["edge_followed_by"]["count"]
            following_count = user["edge_follow"]["count"]
            is_private = user["is_private"]
        except (KeyError, TypeError):
            print(f"Error parsing profile")
        return TProfile(
            id=user_id,
            username=username,
            biography=biography,
            followers_count=followers_count,
            following_count=following_count,
            is_private=is_private)

    @staticmethod
    def page_info(data, endpoint, d_path=None):
        end_cursor = ""
        has_next_page = False
        data_path = d_path or "user"
        try:
            root = data["data"][data_path][endpoint]
            end_cursor = root["page_info"]["end_cursor"]
            has_next_page = root["page_info"]["has_next_page"]
        except (KeyError, TypeError):
            print(f"Error parsing follow_page_info for {endpoint}")
        return TPageInfo(
            end_cursor=end_cursor,
            has_next_page=has_next_page)

    @staticmethod
    def _follow_edge(data, endpoint):
        for edge in Parser._get_edges(data, endpoint):
            node = edge["node"]
            follower = TUser(
                id=node["id"],
                username=node["username"],
                full_name=node["full_name"],
                is_private=node["is_private"]
            )
            yield follower

    @staticmethod
    def timeline(data):
        for edge in Parser._get_edges(data, "edge_owner_to_timeline_media"):
            node = edge["node"]
            post = TTimelinePost(
                id=node["id"],
                timestamp=node["taken_at_timestamp"],
                is_video=node["is_video"],
                like_count=node["edge_media_preview_like"]["count"],
                comment_count=node["edge_media_to_comment"]["count"]
            )
            yield post

    @staticmethod
    def _get_edges(data, endpoint, d_path=None):
        edges = []
        data_path = d_path or "user"
        try:
            root = data["data"][data_path][endpoint]
            edges = root["edges"]
        except (KeyError, TypeError):
            print(f"Error parsing follow_edge for {endpoint}")
        return edges

    @staticmethod
    def story_reel(data):
        try:
            root = data["data"]["reels_media"]
            if root:
                items = root[0]["items"]
                for item in items:
                    post = TStoryReelItem(
                        id=item["id"],
                        timestamp=item["taken_at_timestamp"],
                        expire_at=item["expiring_at_timestamp"],
                        is_video=item["is_video"],
                        view_count=item["edge_story_media_viewers"]["count"],
                        audience=item["audience"]
                    )
                    yield post
        except (KeyError, TypeError):
            print(f"Error parsing story_reel")

    @staticmethod
    def story(data):
        edges = Parser._get_edges(data, "edge_story_media_viewers", "media")
        for edge in edges:
            node = edge["node"]
            viewer = TStoryViewer(
                id=node["id"],
                username=node["username"]
            )
            yield viewer
