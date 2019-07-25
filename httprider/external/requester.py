import requests
from requests.adapters import HTTPAdapter

MAX_RETRIES = 0


class Requester:
    def __init__(self, timeout_secs=5):
        self.timeout_secs = timeout_secs
        self.session = requests.sessions.Session()

    def make_request(self, http_method, resource, kwargs):
        try:
            self.session.mount(resource, HTTPAdapter(
                max_retries=MAX_RETRIES
            ))
            return requests.request(http_method, resource, **kwargs)
        except requests.exceptions.HTTPError as e:
            raise ConnectionError(e)
