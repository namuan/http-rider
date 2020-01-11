import logging
import requests
from requests.adapters import HTTPAdapter

from httprider.core.core_settings import app_settings

MAX_RETRIES = 0


class Requester:
    def __init__(self):
        self.session = requests.sessions.Session()

    def make_request(self, http_method, resource, kwargs):
        app_config = app_settings.load_configuration()
        kwargs["timeout"] = int(app_config.timeout_in_secs)
        kwargs["verify"] = app_config.tls_verification
        kwargs["allow_redirects"] = app_config.allow_redirects

        if app_config.http_proxy and app_config.https_proxy:
            kwargs["proxies"] = {
                "http": app_config.http_proxy,
                "https": app_config.https_proxy,
            }

        try:
            self.session.mount(resource, HTTPAdapter(max_retries=MAX_RETRIES))
            return requests.request(http_method, resource, **kwargs), None
        except requests.exceptions.HTTPError as e:
            return requests.Response(), ConnectionError(e)
        except Exception as e:
            logging.error(e)
            return requests.Response(), e
