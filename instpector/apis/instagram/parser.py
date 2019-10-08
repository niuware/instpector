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
        graphql = data.get("graphql") or {}
        user = graphql.get("user") or {}
        followed_by = user.get("edge_followed_by") or {}
        following = user.get("edge_follow") or {}
        return TProfile(
            id=user.get("id", ""),
            username=user.get("username"),
            biography=user.get("biography"),
            followers_count=followed_by.get("count", 0),
            following_count=following.get("count", 0),
            is_private=user.get("is_private"))

    @staticmethod
    def page_info(data, endpoint, d_path=None):
        data_path = d_path or "user"
        data_root = data.get("data") or {}
        root = data_root.get(data_path) or {}
        endpoint_root = root.get(endpoint) or {}
        page_info = endpoint_root.get("page_info") or {}
        end_cursor = page_info.get("end_cursor", "")
        has_next_page = page_info.get("has_next_page", False)
        return TPageInfo(
            end_cursor=end_cursor,
            has_next_page=has_next_page)

    @staticmethod
    def _follow_edge(data, endpoint):
        for edge in Parser._get_edges(data, endpoint):
            node = edge.get("node") or {}
            follower = TUser(
                id=node.get("id"),
                username=node.get("username"),
                full_name=node.get("full_name"),
                is_private=node.get("is_private")
            )
            yield follower

    @staticmethod
    def timeline(data):
        for edge in Parser._get_edges(data, "edge_owner_to_timeline_media"):
            node = edge.get("node") or {}
            likes = node.get("edge_media_preview_like") or {}
            comments = node.get("edge_media_to_comment") or {}
            display_resources = node.get("display_resources") or {}
            owner = node.get("owner") or {}
            post = TTimelinePost(
                id=node.get("id", ""),
                owner=owner.get("id", ""),
                timestamp=node.get("taken_at_timestamp"),
                is_video=node.get("is_video"),
                like_count=likes.get("count", 0),
                comment_count=comments.get("count", 0),
                display_resources=list(map(lambda res: res.get("src"), display_resources)),
                video_url=node.get("video_url")
            )
            yield post

    @staticmethod
    def _get_edges(data, endpoint, d_path=None):
        data_path = d_path or "user"
        data_root = data.get("data") or {}
        root = data_root.get(data_path) or {}
        endpoint_root = root.get(endpoint) or {}
        return endpoint_root.get("edges") or []

    @staticmethod
    def story_reel(data):
        data_root = data.get("data") or {}
        root = data_root.get("reels_media") or []
        if root:
            items = root[0].get("items") or []
            for item in items:
                viewers = item.get("edge_story_media_viewers") or {}
                display_resources = item.get("display_resources") or {}
                video_resources = item.get("video_resources") or {}
                owner = item.get("owner") or {}
                post = TStoryReelItem(
                    id=item.get("id", ""),
                    owner=owner.get("id", ""),
                    timestamp=item.get("taken_at_timestamp"),
                    expire_at=item.get("expiring_at_timestamp"),
                    is_video=item.get("is_video"),
                    view_count=viewers.get("count"),
                    audience=item.get("audience"),
                    display_resources=list(map(lambda res: res.get("src"), display_resources)),
                    video_resources=list(map(lambda res: res.get("src"), video_resources))
                )
                yield post

    @staticmethod
    def story(data):
        edges = Parser._get_edges(data, "edge_story_media_viewers", "media")
        for edge in edges:
            node = edge.get("node") or {}
            viewer = TStoryViewer(
                id=node.get("id"),
                username=node.get("username")
            )
            yield viewer
