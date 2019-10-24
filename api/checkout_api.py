from typing import TypeVar

import requests

from core.checkout_api_manager import CheckoutAPIManager
from models.checkout_data_models import CheckoutDataModel

PayMayaSDK = TypeVar("PayMayaSDK")


class CheckoutAPI:
    instance: PayMayaSDK
    checkout_data: CheckoutDataModel

    public_api_key: str = None
    secret_api_key: str = None
    environment: str = "SANDBOX"
    encoded_key: str = None

    manager: CheckoutAPIManager

    def __init__(self, *args, **kwargs):
        self.public_api_key = kwargs.get("public_api_key")
        self.secret_api_key = kwargs.get("secret_api_key")
        self.environment = kwargs.get("environment")
        self.encoded_key = kwargs.get("encoded_key", None)
        self.init_manager()

    def init_manager(self):
        manager_data = {
            "public_api_key": self.public_api_key,
            "secret_api_key": self.secret_api_key,
            "environment": self.environment,
        }
        if self.encoded_key:
            manager_data["encoded_key"] = self.encoded_key
        self.manager = CheckoutAPIManager(**manager_data)

    def initiate(self, checkout_data: CheckoutDataModel) -> None:
        self.checkout_data = checkout_data
        self.manager.initiate_checkout(self.checkout_data)

    def execute(self) -> requests.Response:
        return self.manager.execute_checkout()
