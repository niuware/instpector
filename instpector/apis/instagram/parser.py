from .definitions import TUser, TPageInfo, TProfile, TTimelinePost


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
        except KeyError:
            print(f"Error parsing profile")
        return TProfile(
            id=user_id,
            username=username,
            biography=biography,
            followers_count=followers_count,
            following_count=following_count,
            is_private=is_private)

    @staticmethod
    def page_info(data, endpoint):
        end_cursor = ""
        has_next_page = False
        try:
            root = data["data"]["user"][endpoint]
            end_cursor = root["page_info"]["end_cursor"]
            has_next_page = root["page_info"]["has_next_page"]
        except KeyError:
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
    def _get_edges(data, endpoint):
        edges = []
        try:
            root = data["data"]["user"][endpoint]
            edges = root["edges"]
        except KeyError:
            print(f"Error parsing follow_edge for {endpoint}")
        return edges
