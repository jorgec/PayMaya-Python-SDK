from typing import Dict, List

import requests

from core.api_manager import APIManager
from core.constants import (
    PRODUCTION,
    PAYMENTS_PRODUCTION_URL,
    PAYMENTS_SANDBOX_URL,
    PAYMENTS_TOKEN_URL,
    PAYMENTS_URL,
)
from core.http_config import HTTPConfig, HTTP_POST, HTTP_GET
from core.http_connection import HTTPConnection
from models.amount_models import AmountModel
from models.buyer_models import BuyerModel
from models.card_models import CardModel
from models.payment_models import PaymentModel


class PaymentAPIManager(APIManager):
    base_url: str = None
    token: str = None
    token_state: str = None
    status_code: int = None
    buyer: BuyerModel = None
    amount: AmountModel = None
    payments: List = []
    encoded_key: str = None

    def __init__(self, *args, **kwargs):
        self.base_url = self.get_base_url()
        self.encoded_key = kwargs.get("encoded_key", None)
        super().__init__(*args, **kwargs)

    def get_base_url(self) -> str:
        if self.environment == PRODUCTION:
            url = PAYMENTS_PRODUCTION_URL
        else:
            url = PAYMENTS_SANDBOX_URL

        return url

    def create_payment_token(self, card: CardModel = None) -> requests.Response:
        self.use_basic_auth_with_api_key(self.public_api_key)
        http_config = HTTPConfig(
            url=f"{self.base_url}{PAYMENTS_TOKEN_URL}",
            method=HTTP_POST,
            headers=self.http_headers,
        )
        http_connection = HTTPConnection(config=http_config)
        payload = card.serialize()
        response = http_connection.execute(data=payload)

        if response.status_code == 200:
            self.token = response.json().get("paymentTokenId", None)
            self.status_code = response.status_code
            self.token_state = response.json().get("state", None)
        return response

    def execute_payment(
        self, buyer: BuyerModel, amount: AmountModel, redirect_urls: Dict = None
    ) -> requests.Response:
        if not self.token:
            raise ValueError("Cannot pay without token")

        self.use_basic_auth_with_api_key(self.secret_api_key)
        self.buyer = buyer
        self.amount = amount

        http_config = HTTPConfig(
            url=f"{self.base_url}{PAYMENTS_URL}",
            method=HTTP_POST,
            headers=self.http_headers,
        )
        http_connection = HTTPConnection(config=http_config)

        payment_data = {"token": self.token, "buyer": self.buyer, "amount": self.amount}

        if redirect_urls:
            payment_data["urls"] = redirect_urls

        payment = PaymentModel(**payment_data)

        payload = payment.serialize()

        response = http_connection.execute(data=payload)

        try:
            self.payments.append(response.json())
        except AttributeError:
            return response
        except KeyError:
            return response

        return response

    def query_payment(self, payment_id: str) -> Dict:
        data = {}
        self.use_basic_auth_with_api_key(self.secret_api_key)
        http_config = HTTPConfig(
            url=f"{self.base_url}{PAYMENTS_URL}/{payment_id}",
            method=HTTP_GET,
            headers=self.http_headers,
        )
        http_connection = HTTPConnection(config=http_config)

        response = http_connection.execute(data=None)
        if response.status_code == 200:
            data = response.json()
        return data
