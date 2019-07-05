from enum import Enum
from urllib.parse import urlencode

class HttpRequestMode(Enum):
    JSON = 1
    FORM = 2
    NONE = 3

class HttpRequest:
    BROWSER_HEADERS = {
        "User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; "
                       "rv:67.0) Gecko/20100101 Firefox/67.0"),
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "close"
    }
    FORM_HEADERS = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }
    JSON_HEADERS = {
        "Accept": "*/*",
        "X-Requested-With": "XMLHttpRequest"
    }

    def __init__(self, base_url, session):
        self._base_url = base_url
        self._session = session

    def session(self):
        return self._session

    def get(self, url_path, **options):
        request_headers = self._get_headers(
            options.get("mode", HttpRequestMode.JSON),
            options.get("headers"))
        get_params = {}
        if options.get("params"):
            get_params = options.get("params")
        return self._session.get(f"{self._base_url}{url_path}",
                                 headers=request_headers,
                                 params=get_params,
                                 allow_redirects=options.get("redirects", False),
                                 timeout=10)

    def post(self, url_path, data, **options):
        request_headers = self._get_headers(
            options.get("mode", HttpRequestMode.JSON),
            options.get("headers"))
        post_data = urlencode(data)
        post_headers = {**request_headers, "Content-Length": str(len(post_data))}
        return self._session.post(f"{self._base_url}{url_path}",
                                  data=post_data,
                                  headers=post_headers,
                                  allow_redirects=options.get("redirects", False),
                                  timeout=10)

    @classmethod
    def _get_headers(cls, mode, headers):
        request_headers = {}
        custom_headers = {}
        if mode == HttpRequestMode.JSON:
            request_headers = HttpRequest.JSON_HEADERS
        if mode == HttpRequestMode.FORM:
            request_headers = HttpRequest.FORM_HEADERS
        if headers:
            custom_headers = headers
        return {**HttpRequest.BROWSER_HEADERS,
                **request_headers,
                **custom_headers}
