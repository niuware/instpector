class EndpointFactory:
    def __init__(self):
        self._endpoints = {}

    def register_endpoint(self, name, endpoint):
        self._endpoints[name] = endpoint

    def create(self, endpoint_name, instpector):
        endpoint = self._endpoints.get(endpoint_name)
        if not endpoint:
            print(f"No endpoint '{endpoint_name}' available.")
            raise ValueError(endpoint_name)
        return endpoint(instpector)
