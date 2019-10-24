import requests

from core.http_config import HTTPConfig, HTTP_POST, HTTP_GET, HTTP_PUT, HTTP_DELETE


class HTTPConnection:
    http_config = None

    def __init__(self, config: HTTPConfig = None):
        if not HTTPConfig:
            raise ValueError("Config required")

        self.http_config = config

    def execute(self, *, data: None) -> requests.Response:
        """

        :param data: JSON encoded payload
        :return:
        """
        params = {"url": self.http_config.url, "headers": self.http_config.headers}

        if data:
            params["data"] = data

        if self.http_config.method == HTTP_POST:
            response = requests.post(**params)

        elif self.http_config.method == HTTP_GET:
            response = requests.get(**params)
        elif self.http_config.method == HTTP_PUT:
            response = requests.put(**params)
        elif self.http_config.method == HTTP_DELETE:
            response = requests.delete(**params)

        else:
            raise ValueError("Method not implemented!")

        return response
