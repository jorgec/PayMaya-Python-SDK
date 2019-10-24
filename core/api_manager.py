import base64
from typing import Dict


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
