import requests

from core.http_config import HTTPConfig, HTTP_POST


class HTTPConnection:
    http_config = None

    def __init__(self, config: HTTPConfig = None):
        if not HTTPConfig:
            raise ValueError("Config required")

        self.http_config = config

    def execute(self, *, data) -> requests.Response:
        """

        :param data: JSON encoded payload
        :return:
        """
        if self.http_config.method == HTTP_POST:
            response = requests.post(
                url=self.http_config.url, data=data, headers=self.http_config.headers
            )

            return response

        raise ValueError("Not implemented yet")
