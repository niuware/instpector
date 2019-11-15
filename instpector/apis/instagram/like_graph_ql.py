from .base_graph_ql import BaseGraphQL


class LikeGraphQL(BaseGraphQL):

    def __init__(self, instance, url):
        self._url = url
        super().__init__(instance)

    def _toggle_like(self, obj, action):
        endpoint = 'like' if action == 'like' else 'unlike'
        obj_id = getattr(obj, "id", None)
        if obj_id is None:
            return False
        response = self.post(self._url.format(action=endpoint, id=obj_id),
                             use_auth=True,
                             headers={
                                 "Content-Type": "application/x-www-form-urlencoded"
                             })
        if response and response.get("status") == "ok":
            return True
        return False

    def unlike(self, obj):
        return self._toggle_like(obj, 'unlike')

    def like(self, obj):
        return self._toggle_like(obj, 'like')
