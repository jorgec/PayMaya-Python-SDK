import json
from typing import Dict

import requests

from core.constants import (
    REDIRECT_URLS,
    PAYMENTS_TOKEN_URL,
    PAYMENTS_URL,
    PAYMENT_VAULT_CUSTOMERS,
)
from core.http_config import HTTP_PUT, HTTP_DELETE
from core.payment_api_manager import PaymentAPIManager
from models.amount_models import AmountModel
from models.buyer_models import BuyerModel
from models.card_models import CardModel
from models.payment_models import PaymentModel


class PaymentAPI:
    amount: AmountModel = None
    __buyer: BuyerModel = None
    __card: CardModel = None
    redirect_urls: Dict = None

    public_api_key: str = None
    secret_api_key: str = None
    environment: str = "SANDBOX"
    encoded_key: str = None

    manager: PaymentAPIManager

    @property
    def token(self) -> str:
        return self.card.token

    @token.setter
    def token(self, token: str) -> None:
        pass

    @property
    def buyer(self) -> BuyerModel:
        return self.__buyer

    @buyer.setter
    def buyer(self, buyer: BuyerModel) -> None:
        self.__buyer = buyer
        self.__card = None
        self.init_manager()

    @property
    def card(self) -> CardModel:
        return self.__card

    @card.setter
    def card(self, card: CardModel):
        self.__card = card

    def __init__(self, *args, **kwargs):
        self.public_api_key = kwargs.get("public_api_key")
        self.secret_api_key = kwargs.get("secret_api_key")
        self.environment = kwargs.get("environment")
        self.token = ""
        self.card = None
        self.buyer = None
        self.init_manager()

    def init_manager(self):
        manager_data = {
            "public_api_key": self.public_api_key,
            "secret_api_key": self.secret_api_key,
            "environment": self.environment,
        }
        if self.encoded_key:
            manager_data["encoded_key"] = self.encoded_key
        self.manager = PaymentAPIManager(**manager_data)

    def pre_payment_checks(self):
        if not self.card:
            raise AttributeError("No Card")

        if not self.token:
            self.create_token()

        if not self.buyer:
            raise AttributeError("No Buyer")

        if not self.redirect_urls:
            self.redirect_urls = REDIRECT_URLS

    def create_token(self) -> requests.Response:
        if not self.card:
            raise ValueError("No card registered")

        url = f"{self.manager.base_url}{PAYMENTS_TOKEN_URL}"
        result = self.manager.execute(
            url=url, payload=self.card.serialize(), key="public"
        )
        if result.status_code == 200:
            self.card.token = result.json().get("paymentTokenId", None)
            self.card.token_state = result.json().get("state", None)
        return result

    def execute_payment(self) -> requests.Response:
        self.pre_payment_checks()

        if not self.amount:
            raise AttributeError("No Amount")

        url = f"{self.manager.base_url}{PAYMENTS_URL}"
        payment_data = {"token": self.token, "buyer": self.buyer, "amount": self.amount}
        if self.redirect_urls:
            payment_data["urls"] = self.redirect_urls
        payment = PaymentModel(**payment_data)

        result = self.manager.execute(url=url, payload=payment.serialize())
        return result

    def get_payment(self, payment_id: str) -> requests.Response:
        url = f"{self.manager.base_url}{PAYMENTS_URL}/{payment_id}"
        return self.manager.query(url)

    def register_customer(self):
        if not self.buyer:
            raise AttributeError("No Customer/Buyer set")

        url = f"{self.manager.base_url}{PAYMENT_VAULT_CUSTOMERS}"
        result = self.manager.execute(url=url, payload=self.buyer.serialize())

        if result.status_code == 200:
            self.buyer.customer_id = result.json().get("id")
        return result

    def get_customer(self, customer_id: str) -> requests.Response:
        url = f"{self.manager.base_url}{PAYMENT_VAULT_CUSTOMERS}/{customer_id}"
        return self.manager.query(url=url)

    def update_customer(
        self, customer_id: str, fields: Dict = dict
    ) -> requests.Response:
        url = f"{self.manager.base_url}{PAYMENT_VAULT_CUSTOMERS}/{customer_id}"
        payload = json.dumps(fields)
        return self.manager.execute(url=url, payload=payload, method=HTTP_PUT)

    def delete_customer(self, customer_id: str) -> requests.Response:
        url = f"{self.manager.base_url}{PAYMENT_VAULT_CUSTOMERS}/{customer_id}"
        return self.manager.execute(url=url, method=HTTP_DELETE)

    def save_card_to_vault(
        self, is_default: bool = True, redirect_urls: Dict = REDIRECT_URLS
    ):
        self.pre_payment_checks()

        url = f"{self.manager.base_url}{PAYMENT_VAULT_CUSTOMERS}/{self.buyer.customer_id}/cards"
        payload = {
            "paymentTokenId": self.card.token,
            "isDefault": is_default,
            "redirectUrl": redirect_urls,
        }

        return self.manager.execute(url=url, payload=json.dumps(payload))

    def get_cards_in_vault(self):
        if not self.buyer:
            raise AttributeError("No Buyer/Customer set")

        url = f"{self.manager.base_url}{PAYMENT_VAULT_CUSTOMERS}/{self.buyer.customer_id}/cards"
        return self.manager.query(url=url)

    def get_card_in_vault(self, card_token: str):
        if not self.buyer:
            raise AttributeError("No Buyer/Customer set")

        url = f"{self.manager.base_url}{PAYMENT_VAULT_CUSTOMERS}/{self.buyer.customer_id}/cards/{card_token}"
        return self.manager.query(url=url)

    def update_card_in_vault(self, card_token: str, fields: Dict):
        if not self.buyer:
            raise AttributeError("No Buyer/Customer set")

        url = f"{self.manager.base_url}{PAYMENT_VAULT_CUSTOMERS}/{self.buyer.customer_id}/cards/{card_token}"
        payload = json.dumps(fields)

        return self.manager.execute(url=url, payload=payload, method=HTTP_PUT)

    def delete_card_in_vault(self, card_token: str):
        if not self.buyer:
            raise AttributeError("No Buyer/Customer set")

        url = f"{self.manager.base_url}{PAYMENT_VAULT_CUSTOMERS}/{self.buyer.customer_id}/cards/{card_token}"

        return self.manager.execute(url=url, method=HTTP_DELETE)

    def execute_vault_payment(self) -> requests.Response:
        self.pre_payment_checks()

        if not self.amount:
            raise AttributeError("No Amount")

        url = f"{self.manager.base_url}{PAYMENT_VAULT_CUSTOMERS}/{self.buyer.customer_id}/cards/{self.card.token}"
        payload = {"totalAmount": self.amount.as_dict()}

        result = self.manager.execute(url=url, payload=json.dumps(payload))

        return result
