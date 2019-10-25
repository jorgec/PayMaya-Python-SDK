import base64
from typing import Dict

import requests

from core.http_config import HTTP_GET, HTTPConfig, HTTP_POST
from core.http_connection import HTTPConnection


class APIManager:
    public_api_key: str = None
    secret_api_key: str = None
    environment: str = None
    http_headers: Dict = None
    encoded_key: str = None

    def __init__(
        self,
        public_api_key: str,
        secret_api_key: str,
        environment: str = "SANDBOX",
        encoded_key: str = None,
    ):
        self.public_api_key = public_api_key
        self.secret_api_key = secret_api_key
        self.environment = environment
        self.http_headers = {"Content-Type": "application/json"}
        if encoded_key:
            self.encoded_key = encoded_key

    def use_basic_auth_with_api_key(self, api_key: str = None):
        if not api_key and not self.encoded_key:
            raise ValueError("API Key is required")

        if self.encoded_key:
            token = self.encoded_key
        else:
            token = base64.b64encode(api_key.encode("utf-8")).decode()
        self.http_headers["Authorization"] = f"Basic {token}:"

    def execute(
        self, url: str, key: str = "secret", method: str = HTTP_POST, payload=None
    ) -> requests.Response:
        if key == "public":
            api_key = self.public_api_key
        else:
            api_key = self.secret_api_key

        self.use_basic_auth_with_api_key(api_key)

        http_config = HTTPConfig(url=url, method=method, headers=self.http_headers)
        http_connection = HTTPConnection(config=http_config)

        return http_connection.execute(data=payload)

    def query(
        self, key: str = "secret", method: str = HTTP_GET, url: str = None
    ) -> requests.Response:
        if key == "public":
            api_key = self.public_api_key
        else:
            api_key = self.secret_api_key

        self.use_basic_auth_with_api_key(api_key)

        http_config = HTTPConfig(url=url, method=method, headers=self.http_headers)
        http_connection = HTTPConnection(config=http_config)

        response = http_connection.execute(data=None)
        return response
