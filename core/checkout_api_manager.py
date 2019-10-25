from typing import List

import requests

from core.api_manager import APIManager
from core.constants import (
    PRODUCTION,
    CHECKOUT_PRODUCTION_URL,
    CHECKOUT_SANDBOX_URL,
    CHECKOUTS_URL,
)
from models.checkout_data_models import CheckoutDataModel


class CheckoutAPIManager(APIManager):
    base_url: str = None
    checkout_data: CheckoutDataModel = None
    checkouts: List = []

    def __init__(self, *args, **kwargs):
        self.base_url = self.get_base_url()
        super().__init__(*args, **kwargs)

    def get_base_url(self) -> str:
        if self.environment == PRODUCTION:
            url = CHECKOUT_PRODUCTION_URL
        else:
            url = CHECKOUT_SANDBOX_URL

        return url

    def initiate_checkout(self, checkout_data: CheckoutDataModel) -> None:
        """
        Placeholder method in case we need to do some more pre-processing later
        :param checkout_data:
        :return:
        """
        self.checkout_data = checkout_data

    def execute_checkout(self) -> requests.Response:
        if not self.checkout_data:
            raise ValueError("No Checkout Data")

        url = f"{self.base_url}{CHECKOUTS_URL}"

        return self.execute(url=url, payload=self.checkout_data.serialize())
