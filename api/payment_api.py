from typing import Dict

import requests

from core.constants import REDIRECT_URLS
from core.payment_api_manager import PaymentAPIManager
from models.amount_models import AmountModel
from models.buyer_models import BuyerModel
from models.card_models import CardModel


class PaymentAPI:
    amount: AmountModel = None
    __buyer: BuyerModel = None
    __card: CardModel = None
    redirect_urls: Dict = None

    public_api_key: str = None
    secret_api_key: str = None
    environment: str = "SANDBOX"

    manager: PaymentAPIManager

    @property
    def token(self) -> str:
        return self.manager.token

    @token.setter
    def token(self, *args, **kwargs) -> None:
        pass

    @property
    def buyer(self) -> BuyerModel:
        return self.__buyer

    @buyer.setter
    def buyer(self, buyer: BuyerModel) -> None:
        self.__buyer = buyer
        self.__card = None

    @property
    def card(self) -> CardModel:
        return self.__card

    @card.setter
    def card(self, card: CardModel):
        self.__card = card
        self.init_manager()

    def __init__(self, *args, **kwargs):
        self.public_api_key = kwargs.get("public_api_key")
        self.secret_api_key = kwargs.get("secret_api_key")
        self.environment = kwargs.get("environment")
        self.init_manager()

    def init_manager(self):
        self.manager = PaymentAPIManager(
            public_api_key=self.public_api_key,
            secret_api_key=self.secret_api_key,
            environment=self.environment,
        )

    def create_token(self) -> requests.Response:
        if not self.card:
            raise ValueError("No card registered")

        result = self.manager.create_payment_token(card=self.card)
        return result

    def execute_payment(self) -> requests.Response:
        if not self.token:
            raise AttributeError("No Token")

        if not self.buyer:
            raise AttributeError("No Buyer")

        if not self.amount:
            raise AttributeError("No Amount")

        if not self.redirect_urls:
            self.redirect_urls = REDIRECT_URLS

        result = self.manager.execute_payment(
            buyer=self.buyer, amount=self.amount, redirect_urls=self.redirect_urls
        )

        return result

    def query_payment(self, payment_id: str) -> requests.Response:
        return self.manager.query_payment(payment_id)

    def register_customer(self):
        if not self.buyer:
            raise AttributeError("No Customer/Buyer set")

        return self.manager.register_customer(customer=self.buyer)

    def query_customer(self, customer_id: str) -> requests.Response:
        return self.manager.query_customer(customer_id)

    def update_customer(
        self, customer_id: str, fields: Dict = dict
    ) -> requests.Response:
        return self.manager.update_customer(customer_id=customer_id, fields=fields)

    def delete_customer(self, customer_id: str) -> requests.Response:
        return self.manager.delete_customer(customer_id)
