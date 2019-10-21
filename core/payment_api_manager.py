import base64
from typing import Dict, List

import requests

from core.constants import PRODUCTION, PAYMENTS_PRODUCTION_URL, PAYMENTS_SANDBOX_URL, PAYMENTS_TOKEN_URL, PAYMENTS_URL
from core.http_config import HTTPConfig, HTTP_POST
from core.http_connection import HTTPConnection
from models.amount import Amount
from models.buyer import Buyer
from models.card import Card
from models.payment import Payment as PaymentModel
from paymaya_sdk import PayMayaSDK


class PaymentAPIManager:
    public_api_key: str = None
    secret_api_key: str = None
    environment: str = None
    base_url: str = None
    http_headers: Dict = None
    token: str = None
    token_state: str = None
    status_code: int = None
    buyer: Buyer = None
    amount: Amount = None
    payments: List = []

    def __init__(self):
        instance = PayMayaSDK.get_instance()
        self.public_api_key = instance.payments_public_api_key
        self.secret_api_key = instance.payments_secret_api_key
        self.environment = instance.payments_environment
        self.base_url = self.get_base_url()
        self.http_headers = {"Content-Type": "application/json"}

    def get_base_url(self) -> str:
        if self.environment == PRODUCTION:
            url = PAYMENTS_PRODUCTION_URL
        else:
            url = PAYMENTS_SANDBOX_URL

        return url

    def use_basic_auth_with_api_key(self, api_key: str = None):
        if not api_key:
            raise ValueError("API Key is required")

        token = base64.b64encode(api_key.encode("utf-8"))
        self.http_headers["Authorization"] = f"Basic {token.decode()}:"

    def create_payment_token(self, card: Card = None) -> requests.Response:
        self.use_basic_auth_with_api_key(self.public_api_key)
        http_config = HTTPConfig(
            url=f"{self.base_url}{PAYMENTS_TOKEN_URL}",
            method=HTTP_POST,
            headers=self.http_headers,
        )
        http_connection = HTTPConnection(config=http_config)
        payload = card.serialize()
        response = http_connection.execute(data=payload)

        try:
            self.token = response.json().get('paymentTokenId', None)
            self.status_code = response.status_code
            self.token_state = response.json().get('state', None)

        except AttributeError:
            pass

        return response

    def charge_card(self, buyer: Buyer, amount: Amount, redirect_urls: Dict = None):
        if not self.token:
            raise ValueError("Cannot pay without token")

        self.use_basic_auth_with_api_key(self.secret_api_key)
        self.buyer = buyer
        self.amount = amount

        http_config = HTTPConfig(
            url=f"{self.base_url}{PAYMENTS_URL}",
            method=HTTP_POST,
            headers=self.http_headers
        )
        http_connection = HTTPConnection(config=http_config)

        payment_data = {
            'token': self.token,
            'buyer': self.buyer,
            'amount': self.amount
        }

        if redirect_urls:
            payment_data['urls'] = redirect_urls

        payment = PaymentModel(
            **payment_data
        )

        payload = payment.serialize()

        response = http_connection.execute(data=payload)

        try:
            self.payments.append(response.json())
        except AttributeError:
            pass

        return response
