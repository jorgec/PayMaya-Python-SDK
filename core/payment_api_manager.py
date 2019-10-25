import json
from typing import Dict

import requests

from core.api_manager import APIManager
from core.constants import (
    PRODUCTION,
    PAYMENTS_PRODUCTION_URL,
    PAYMENTS_SANDBOX_URL,
    PAYMENTS_TOKEN_URL,
    PAYMENTS_URL,
    PAYMENT_VAULT_CUSTOMERS,
)
from core.http_config import HTTP_PUT, HTTP_DELETE
from models.amount_models import AmountModel
from models.buyer_models import BuyerModel
from models.card_models import CardModel
from models.payment_models import PaymentModel


class PaymentAPIManager(APIManager):
    base_url: str = None

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

    def create_payment_token(self, card: CardModel) -> requests.Response:
        url = f"{self.base_url}{PAYMENTS_TOKEN_URL}"
        return self.execute(url=url, payload=card.serialize(), key="public")

    def execute_payment(
        self,
        token: str,
        buyer: BuyerModel,
        amount: AmountModel,
        redirect_urls: Dict = None,
    ) -> requests.Response:

        url = f"{self.base_url}{PAYMENTS_URL}"
        payment_data = {"token": token, "buyer": buyer, "amount": amount}
        if redirect_urls:
            payment_data["urls"] = redirect_urls
        payment = PaymentModel(**payment_data)
        return self.execute(url=url, payload=payment.serialize())

    def get_payment(self, payment_id: str) -> requests.Response:
        url = f"{self.base_url}{PAYMENTS_URL}/{payment_id}"
        return self.query(url)

    def register_customer(self, customer: BuyerModel) -> requests.Response:
        url = f"{self.base_url}{PAYMENT_VAULT_CUSTOMERS}"
        return self.execute(url=url, payload=customer.serialize())

    def get_customer(self, customer_id: str) -> requests.Response:
        url = f"{self.base_url}{PAYMENT_VAULT_CUSTOMERS}/{customer_id}"
        return self.query(url=url)

    def update_customer(self, customer_id: str, fields: Dict = dict):
        url = f"{self.base_url}{PAYMENT_VAULT_CUSTOMERS}/{customer_id}"
        payload = json.dumps(fields)
        return self.execute(url=url, payload=payload, method=HTTP_PUT)

    def delete_customer(self, customer_id: str):
        url = f"{self.base_url}{PAYMENT_VAULT_CUSTOMERS}/{customer_id}"
        return self.execute(url=url, method=HTTP_DELETE)

    def save_card_to_vault(
        self, buyer: BuyerModel, card: CardModel, is_default: bool, redirect_urls: Dict
    ) -> requests.Response:
        url = f"{self.base_url}{PAYMENT_VAULT_CUSTOMERS}/{buyer.customer_id}/cards"
        payload = {
            "paymentTokenId": card.token,
            "isDefault": is_default,
            "redirectUrl": redirect_urls,
        }
        return self.execute(url=url, payload=json.dumps(payload))

    def get_cards_in_vault(self, buyer: BuyerModel) -> requests.Response:
        url = f"{self.base_url}{PAYMENT_VAULT_CUSTOMERS}/{buyer.customer_id}/cards"
        return self.query(url=url)

    def get_card_in_vault(
        self, buyer: BuyerModel, card_token: str
    ) -> requests.Response:
        url = f"{self.base_url}{PAYMENT_VAULT_CUSTOMERS}/{buyer.customer_id}/cards/{card_token}"
        return self.query(url=url)

    def update_card_in_vault(
        self, buyer: BuyerModel, card_token: str, fields: Dict
    ) -> requests.Response:
        url = f"{self.base_url}{PAYMENT_VAULT_CUSTOMERS}/{buyer.customer_id}/cards/{card_token}"
        payload = json.dumps(fields)
        return self.execute(url=url, payload=payload, method=HTTP_PUT)

    def delete_card_in_vault(
        self, buyer: BuyerModel, card_token: str
    ) -> requests.Response:
        url = f"{self.base_url}{PAYMENT_VAULT_CUSTOMERS}/{buyer.customer_id}/cards/{card_token}"
        return self.execute(url=url, method=HTTP_DELETE)

    def execute_vault_payment(
        self, buyer: BuyerModel, card: CardModel, amount: AmountModel
    ):
        url = f"{self.base_url}{PAYMENT_VAULT_CUSTOMERS}/{buyer.customer_id}/cards/{card.token}"
        payload = {"totalAmount": amount.as_dict()}
        return self.execute(url=url, payload=json.dumps(payload))
