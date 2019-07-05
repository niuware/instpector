import json
from .http_request import HttpRequest
from .exceptions import ParseDataException

class BaseApi(HttpRequest):
    def get(self, url_path, **options):
        response = super().get(url_path, **options)
        if response.status_code == 200:
            try:
                return json.loads(response.text)
            except json.decoder.JSONDecodeError:
                raise ParseDataException
        return None
