import pytest
from instpector import endpoints

@pytest.mark.incremental
class TestApi:
    user_id = None
    story_id = None
    def test_profile(self, instance, username):
        profile = endpoints.factory.create("profile", instance)
        user = profile.of_user(username)
        assert type(user).__name__ == "TProfile"
        TestApi.user_id = user.id
        assert user.username == username

    def test_followers(self, instance):
        followers = endpoints.factory.create("followers", instance)
        first = None
        for follower in followers.of_user(TestApi.user_id):
            first = follower
            break
        assert type(first).__name__ == "TUser"
        assert first.id != ""
        assert first.username != ""

    def test_following(self, instance):
        following = endpoints.factory.create("following", instance)
        first = None
        for followee in following.of_user(TestApi.user_id):
            first = followee
            break
        assert type(first).__name__ == "TUser"
        assert first.id != ""
        assert first.username != ""

    def test_timeline(self, instance):
        timeline = endpoints.factory.create("timeline", instance)
        first = None
        for post in timeline.of_user(TestApi.user_id):
            first = post
            break
        assert type(first).__name__ == "TTimelinePost"
        assert first.id != ""

    def test_story_reel(self, instance):
        story_reel = endpoints.factory.create("story_reel", instance)
        first = None
        for story_item in story_reel.of_user(TestApi.user_id):
            first = story_item
            break
        assert type(first).__name__ == "TStoryReelItem"
        TestApi.story_id = first.id

    def test_story(self, instance):
        story = endpoints.factory.create("story", instance)
        first = None
        for viewer in story.viewers_for(TestApi.story_id):
            first = viewer
            break
        assert type(first).__name__ == "TStoryViewer"
        assert first.id != ""
