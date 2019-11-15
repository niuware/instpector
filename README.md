# Instpector

A simple Instagram's web API library written in Python. Supports login with two-factor authentication enabled. No selenium or webdriver required.

## Installation

```
pip install instpector
```

# Sample usage

```python
from instpector import Instpector, endpoints

instpector = Instpector()
instpector.login("my_username", "my_password")

profile = endpoints.factory.create("profile", instpector)
followers = endpoints.factory.create("followers", instpector)

insta_profile = profile.of_user("some_username")

# Loop through all followers
for follower in followers.of_user(insta_profile.id):
    print(follower.username)

instpector.logout()
```

## Using 2FA
For login in using two-factor authentication, generate your 2fa key once on the  Instagram's app and provide the code when logging in with `instpector`. The following example uses `pytop` library to demonstrate the usage:

```python
from pyotp import TOTP
from instpector import Instpector, endpoints

instpector = Instpector()
totp = TOTP("my_2fa_key") # Input without spaces

# Login into Instagram's web
instpector.login("my_username", "my_password", totp.now())
```

# Examples

Check out more examples [here](https://github.com/niuware/instpector/tree/master/examples).

# Endpoints

- Followers   
- Following   
- Timeline   
- Comments
- Profile   
- Story Reel    
- Story    

More to come

# API

## Classes

`Instpector`

|Method|Details|
|---|---|
|login(user: `string`, password: `string`, two_factor_code: `string` = None)|Login to an Instagram account. If your account is 2FA protected provide the 2FA code as in the [provided example](https://github.com/niuware/instpector/blob/master/examples/two_factor_auth.py).|
|logout()|Logouts from an Instagram account|
|session()|Returns the current session used by `instpector`|

`EndpointFactory`

|Method|Details|
|---|---|
|create(endpoint_name: `string`, instpector_instance: `Instpector`)|Creates and returns an endpoint instance based on the provided name. Available endpoint names are: `"followers"`, `"following"`, `"profile"`, `"timeline"`, `"comments"` `"story_reel"` and `"story"`|

## Endpoints

### Profile

Gets the profile of any public or friend user account.

|Method|Details|
|---|---|
|of_user(username: `string`)|Returns a `TProfile` instance for the provided username.|

### Followers

Endpoint for accessing the follower list of any public or friend user account.

|Method|Details|
|---|---|
|of_user(user_id: `string`)|Returns a generator of `TUser` instances with all followers. Note the method receives a user id and not a username. To get the user id use the `Profile` endpoint.|

### Following

Endpoint for accessing the followees list of any public or friend user account.

|Method|Details|
|---|---|
|of_user(user_id: `string`)|Returns a generator of `TUser` instances with all followees. Note the method receives a user id and not a username. To get the user id use the `Profile` endpoint.|

### Timeline

Endpoint for accessing the timeline of any public or friend account.

|Method|Details|
|---|---|
|of_user(user_id: `string`)|Returns a generator of `TTimelinePost` instances with all timeline posts. Note the method receives a user id and not a username. To get the user id use the `Profile` endpoint.|
|download(timeline_post: `TTimelinePost`, only_image: `bool` = False, low_quality: `bool` = False)|Downloads and save the available resources (image and video) for the provided `TTimelinePost`. The file name convention is `ownerid_resourceid.extension` and saved in the execution directory. If `low_quality` is `True` the resource will be the downloaded with the lowest size available (only for image). If `only_image` is `True` a video file resource won't be downloaded.|
|like(timeline_post: `TTimelinePost`)|Likes a timeline post.|
|unlike(timeline_post: `TTimelinePost`)|Unlikes a timeline post.|

### Comments

Endponint for accessing comments and threaded comments of any public or friends post or comment.

|Method|Details|
|---|---|
|of_post(timeline_post: `TTimelinePost`)|Returns a generator of `TComment` instances with all post comments.|
|of_comment(comment: `TComment`)|Returns a generator of `TComment` instances with all threaded comments of a comment.|
|like(comment: `TComment`)|Likes a comment.|
|unlike(comment: `TComment`)|Unlikes a comment.|

### StoryReel

Endpoint for accessing the story reel (stories) of any public or friend user account.

|Method|Details|
|---|---|
|of_user(user_id: `string`)|Returns a generator of `TStoryReelItem` instances with all stories. Note the method receives a user id and not a username. To get a user id use the `Profile` endpoint.|
|download(story_item: `TStoryReelItem`, only_image: `bool` = False, low_quality: `bool` = False)|Downloads and save the available resources (image and video) for the provided `TStoryReelItem`. The file name convention is `ownerid_resourceid.extension` and saved in the execution directory. If `low_quality` is `True` the resource will be the downloaded with the lowest size available. If `only_image` is `True` a video file resource won't be downloaded.|

### Story

Endpoint for accessing the story details of a story reel item. This endpoint is only available for stories posted by the current logged in user.

|Method|Details|
|---|---|
|viewers_for(story_id: `string`)|Returns a generator of `TStoryViewer` instances with all viewers of the provided story id.|

## Types

### TUser

|Field|Type|Details|
|---|---|---|
|id|`string`|The Instagram Id of the user|
|username|`string`|The user's name|
|full_name|`string`|The full name of the user|
|is_private|`bool`|A flag to show if the user account is private|

### TProfile

|Field|Type|Details|
|---|---|---|
|id|`string`|The Instagram Id of the user|
|username|`string`|The user's name|
|biography|`string`|The biography of the user|
|is_private|`bool`|A flag to show if the user account is private|
|followers_count|`integer`|The follower count of the user|
|following_count|`integer`|The following count of the user|

### TTimelinePost
|Field|Type|Details|
|---|---|---|
|id|`string`|The Instagram Id of the user|
|owner|`string`|The owner account Instagram Id|
|timestamp|`integer`|The timestamp of the post|
|is_video|`bool`|A flag to know if the story is a video|
|like_count|`integer`|The like count of the post|
|comment_count|`integer`|The comment count of the post|
|display_resources|`list`|A list of image URLs associated with the post|
|video_url|`string`|The video URL (if available) associated with the post|

### TComment
|Field|Type|Details|
|---|---|---|
|id|`string`|The Instagram Id of the comment|
|text|`string`|The comment text|
|username|`string`|The author's username|
|timestamp|`integer`|The timestamp of the comment|
|viewer_has_liked|`bool`|A flag to know if the viewer liked the comment|
|liked_count|`integer`|The like count of the comment|
|thread_count|`integer` \| `None`|The comment's thread comments count. This value is `None` if the instance is a threaded comment.|

### TStoryReelItem
|Field|Type|Details|
|---|---|---|
|id|`string`|The Instagram Id of the story|
|owner|`string`|The owner account Instagram Id|
|timestamp|`integer`|The timestamp of the story|
|expire_at|`integer`|The expiration timestamp of the story|
|audience|`string`|The type of audience of the story. If public the value is `MediaAudience.DEFAULT`, if private the value is `MediaAudience.BESTIES`|
|is_video|`bool`|A flag to know if the story is a video|
|view_count|`integer`|The view count of the story. The count is only available for stories posted by the currently logged in user. Other accounts will have a count equal to `0`.|
|display_resources|`list`|A list of image URLs associated with the story|
|video_resources|`list`|A list of video URLs associated with the story|

### TStoryViewer
|Field|Type|Details|
|---|---|---|
|id|`string`|The Instagram Id of the story viewer|
|username|`string`|The user name of the viewer|

# Development dependencies

- requests

# Tests

1. Create a `pytest.ini` file with the sample contents of  `pytest.sample.ini` in the `tests` directory.

2. Add your account information. 
3. Run with `pytest`:
```
(env)$ pytest -qs tests
```

# Disclaimer

This tool is not affiliated with, authorized, maintained or endorsed by Instagram or any of its affiliates or subsidiaries. Use at your own risk.

# License

Licensed under MIT License.