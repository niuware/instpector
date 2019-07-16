import json
from os import path
from instpector.apis.instagram.parser import Parser

def test_followers(followers_file=None):
    json_file = "tests/followers.json"
    if followers_file:
        json_file = followers_file
    if path.isfile(json_file):
        data = json.loads(open(json_file, "r").read())
        for follower in Parser.followers(data):
            print(follower)

def test_following(following_file=None):
    json_file = "tests/following.json"
    if following_file:
        json_file = following_file
    if path.isfile(json_file):
        data = json.loads(open(json_file, "r").read())
        for followee in Parser.following(data):
            print(followee)

def test_profile(profile_file=None):
    json_file = "tests/profile.json"
    if profile_file:
        json_file = profile_file
    if path.isfile(json_file):
        data = json.loads(open(json_file, "r").read())
        print(Parser.profile(data))

def test_timeline(timeline_file=None):
    json_file = "tests/timeline.json"
    if timeline_file:
        json_file = timeline_file
    if path.isfile(json_file):
        data = json.loads(open(json_file, "r").read())
        for post in Parser.timeline(data):
            print(post)

def test_story_reel(story_reel_file=None):
    json_file = "tests/story_reel.json"
    if story_reel_file:
        json_file = story_reel_file
    if path.isfile(json_file):
        data = json.loads(open(json_file, "r").read())
        for item in Parser.story_reel(data):
            print(item)

def test_story(story_file=None):
    json_file = "tests/story.json"
    if story_file:
        json_file = story_file
    if path.isfile(json_file):
        data = json.loads(open(json_file, "r").read())
        for item in Parser.story(data):
            print(item)
