from collections import namedtuple

TUser = namedtuple("TUser", "id username full_name is_private")

TPageInfo = namedtuple("TPageInfo", "end_cursor has_next_page")

TProfile = namedtuple("TProfile", (
    "id username biography is_private followers_count following_count"
))

TTimelinePost = namedtuple("TTimelinePost", (
    "id owner timestamp is_video like_count comment_count display_resources video_url shortcode"
))

TStoryReelItem = namedtuple("TStoryReelItem", (
    "id owner timestamp expire_at audience is_video view_count display_resources video_resources"
))

TStoryViewer = namedtuple("TStoryViewer", "id username")

TComment = namedtuple("TComment", (
    "id text timestamp username viewer_has_liked liked_count, thread_count"
))
