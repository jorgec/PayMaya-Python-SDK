from typing import TypeVar, Generic

from core.checkout_api_manager import CheckoutAPIManager
from models.checkout_data_models import CheckoutDataModel

PayMayaSDK = TypeVar("PayMayaSDK")


class CheckoutAPI:
    instance: PayMayaSDK
    checkout_data: CheckoutDataModel

    manager: CheckoutAPIManager

    def __init__(self, instance: Generic[PayMayaSDK], encoded_key: str = None):
        self.instance = instance
        if encoded_key:
            self.manager = CheckoutAPIManager(instance, encoded_key)
        else:
            self.manager = CheckoutAPIManager(instance)

    def initiate(self, checkout_data: CheckoutDataModel) -> None:
        self.checkout_data = checkout_data
        self.manager.initiate_checkout(self.checkout_data)

    def execute(self) -> bool:
        return self.manager.execute_checkout()
