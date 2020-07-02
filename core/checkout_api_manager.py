from typing import List

from core.api_manager import APIManager
from core.constants import PRODUCTION, CHECKOUT_PRODUCTION_URL, CHECKOUT_SANDBOX_URL
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
