import contextlib

from call.endpoint import Endpoint


class EndpointManager:
    def __init__(self, data):
        self.data = data

    def __iter__(self):
        for key in self.data:
            with self.get_endpoint(key) as endpoint:
                yield endpoint

    def __contains__(self, name):
        return name in self.data

    @contextlib.contextmanager
    def get_endpoint(self, alias):
        endpoint = Endpoint.from_dict(self.data[alias])
        try:
            yield endpoint
        finally:
            self.data[alias] = endpoint.to_dict()
