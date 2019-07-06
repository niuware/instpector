import json
from time import sleep
from ..http_request import HttpRequest
from ..exceptions import ParseDataException

class BaseApi(HttpRequest):
    def get(self, url_path, **options):
        response = super().get(url_path, **options)
        # Retry just once when rate limit has been exceeded
        if response.status_code == 429:
            print("The rate limit has been reached. Resuming in 3 min...")
            sleep(180)
            response = super().get(url_path, **options)
        if response.status_code == 200:
            try:
                return json.loads(response.text)
            except json.decoder.JSONDecodeError:
                raise ParseDataException
        return None
