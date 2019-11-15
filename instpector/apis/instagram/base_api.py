import json
from time import sleep
from ..http_request import HttpRequest
from ..exceptions import ParseDataException

class BaseApi(HttpRequest):
    def get(self, url_path, **options):
        response = super().get(url_path, **options)
        if not response:
            return None
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

    def post(self, url_path, data=None, **options):
        response = super().post(url_path, data or {}, **options)
        if response.status_code == 200:
            try:
                return json.loads(response.text)
            except json.decoder.JSONDecodeError:
                raise ParseDataException
        return None

    def quick_post(self, url_path, data=None, **options):
        response = self.post(url_path, data=data, use_auth=True,
                             headers={
                                 "Content-Type": "application/x-www-form-urlencoded"
                             },
                             **options)
        if response and response.get("status") == "ok":
            return True
        return False

    def _download_resources_list(self, item, name, extension, low_quality):
        try:
            resources = getattr(item, name)
        except AttributeError:
            return
        if resources:
            quality = (len(resources) - 1) if not low_quality else 0
            file_name = f"{item.owner}_{item.id}.{extension}"
            super().download_file(resources[quality], file_name)
