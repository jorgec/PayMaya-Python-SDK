import base64
from typing import Dict, TypeVar, Generic, List

from core.constants import (
    PRODUCTION,
    CHECKOUT_PRODUCTION_URL,
    CHECKOUT_SANDBOX_URL,
    CHECKOUTS_URL,
)
from core.http_config import HTTPConfig, HTTP_POST
from core.http_connection import HTTPConnection
from models.checkout_data_models import CheckoutDataModel


PayMayaSDK = TypeVar("PayMayaSDK")


class CheckoutAPIManager:
    public_api_key: str = None
    secret_api_key: str = None
    environment: str = None
    base_url: str = None
    http_headers: Dict = None
    checkout_data: CheckoutDataModel = None
    checkouts: List = []
    encoded_key: str

    def __init__(self, instance: Generic[PayMayaSDK], encoded_key: str = ""):
        self.public_api_key = instance.public_api_key
        self.secret_api_key = instance.secret_api_key
        self.environment = instance.environment
        self.base_url = self.get_base_url()
        self.http_headers = {"Content-Type": "application/json"}
        self.encoded_key = encoded_key

    def get_base_url(self) -> str:
        if self.environment == PRODUCTION:
            url = CHECKOUT_PRODUCTION_URL
        else:
            url = CHECKOUT_SANDBOX_URL

        return url

    def use_basic_auth_with_api_key(self, api_key: str = None):
        if not api_key and not self.encoded_key:
            raise ValueError("API Key is required")

        if self.encoded_key:
            token = self.encoded_key
        else:
            token = base64.b64encode(api_key.encode("utf-8")).decode()
            self.encoded_key = token
        self.http_headers["Authorization"] = f"Basic {token}:"

    def initiate_checkout(self, checkout_data: CheckoutDataModel):
        self.checkout_data = checkout_data

    def execute_checkout(self) -> bool:
        if not self.checkout_data:
            raise ValueError("No Checkout Data")

        self.use_basic_auth_with_api_key(self.secret_api_key)

        http_config = HTTPConfig(
            url=f"{self.base_url}{CHECKOUTS_URL}",
            method=HTTP_POST,
            headers=self.http_headers,
        )
        http_connection = HTTPConnection(config=http_config)

        payload = self.checkout_data.serialize()

        response = http_connection.execute(data=payload)

        self.checkouts.append(response)

        if response.status_code == 200:
            return True
        return False
