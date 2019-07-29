import requests
import pytest
from instpector.apis.instagram.utilities import get_ajax_id, get_consumer_lib_path, get_app_id

@pytest.mark.incremental
class TestUtilities:
    js_path = ""
    def test_get_ajax_id(self, base_url):
        html = requests.get(base_url, stream=True)
        assert get_ajax_id(html.text) != ""

    def test_get_consumer_lib_path(self, base_url):
        html = requests.get(base_url, stream=True)
        TestUtilities.js_path = get_consumer_lib_path(html.iter_lines(decode_unicode=True))
        assert TestUtilities.js_path != ""

    def test_get_app_id(self, base_url):
        js_file = requests.get(f"{base_url}{TestUtilities.js_path}")
        assert get_app_id(js_file.text)
