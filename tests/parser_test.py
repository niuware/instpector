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
