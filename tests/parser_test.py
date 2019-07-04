import json
from os import path
from instpector.apis.instagram.parser import Parser

def test_followers_parse(test_file=None):
    json_file = "tests/followers.json"
    if test_file:
        json_file = test_file
    if path.isfile(json_file):
        data = json.loads(open(json_file, "r").read())
        for follower in Parser.followers(data):
            print(follower)
