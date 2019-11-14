from enum import Enum
from urllib.parse import urlencode
from requests import RequestException, HTTPError

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

    def __init__(self, base_url, instance):
        self._base_url = base_url
        self._auth_headers = instance.auth_headers()
        self._session = instance.session()

    def session(self):
        return self._session

    def get(self, url_path, **options):
        request_headers = self._get_headers(**options)
        get_params = {}
        if options.get("params"):
            get_params = options.get("params")
        try:
            return self._session.get(f"{self._base_url}{url_path}",
                                     headers=request_headers,
                                     params=get_params,
                                     allow_redirects=options.get("redirects", False),
                                     timeout=10)
        except RequestException as req_exception:
            print(f"GET RequestException: {req_exception}")
            return None

    def post(self, url_path, data, **options):
        request_headers = self._get_headers(**options)
        post_data = urlencode(data)
        post_headers = {**request_headers, "Content-Length": str(len(post_data))}
        try:
            return self._session.post(f"{self._base_url}{url_path}",
                                      data=post_data,
                                      headers=post_headers,
                                      allow_redirects=options.get("redirects", False),
                                      timeout=10)
        except RequestException as req_exception:
            print(f"POST RequestException: {req_exception}")
            return None

    def download_file(self, url, filename):
        with self._session.get(url, stream=True) as req:
            try:
                req.raise_for_status()
            except HTTPError:
                print(f"Failed to download file at {url}")
                return
            with open(filename, 'wb') as downloaded_file:
                for chunk in req.iter_content(chunk_size=8192):
                    if chunk:
                        downloaded_file.write(chunk)

    def _get_headers(self, **options): #mode, headers, use_auth=False):
        request_headers = {}
        custom_headers = {}
        auth_headers = {}
        mode = options.pop("mode", HttpRequestMode.JSON)
        headers = options.pop("headers", None)
        use_auth = options.pop("use_auth", False)
        # JSON Request headers
        if mode == HttpRequestMode.JSON:
            request_headers = HttpRequest.JSON_HEADERS
        # Form Request headers
        if mode == HttpRequestMode.FORM:
            request_headers = HttpRequest.FORM_HEADERS
        # Custom headers
        if headers:
            custom_headers = headers
        # Authenticated headers
        if use_auth:
            auth_headers = self._auth_headers
        return {**HttpRequest.BROWSER_HEADERS,
                **request_headers,
                **custom_headers,
                **auth_headers}
