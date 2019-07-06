from os import path
from instpector.apis.instagram.utilities import get_ajax_id, get_consumer_lib_path, get_app_id

def test_get_ajax_id(index_file=None):
    html_file = "tests/index.html"
    if index_file:
        html_file = index_file
    if path.isfile(html_file):
        with open(html_file, "r") as data:
            print(get_ajax_id(data.read()))

def test_get_consumer_lib_path(index_file=None):
    html_file = "tests/index.html"
    if index_file:
        html_file = index_file
    if path.isfile(html_file):
        with open(html_file, "r") as data:
            print(get_consumer_lib_path(data.readlines()))

def test_get_app_id(consumerlib_file=None):
    js_file = "tests/consumerlib.js"
    if consumerlib_file:
        js_file = consumerlib_file
    if path.isfile(js_file):
        with open(js_file, "r") as data:
            print(get_app_id(data.read()))
