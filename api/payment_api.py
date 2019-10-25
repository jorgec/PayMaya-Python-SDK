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
    encoded_key: str = None
    redirect_urls: Dict = None

    public_api_key: str = None
    secret_api_key: str = None
    environment: str = "SANDBOX"

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
        self.manager = PaymentAPIManager(
            public_api_key=self.public_api_key,
            secret_api_key=self.secret_api_key,
            environment=self.environment,
        )

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

        result = self.manager.create_payment_token(card=self.card)
        if result.status_code == 200:
            self.card.token = result.json().get("paymentTokenId", None)
            self.card.token_state = result.json().get("state", None)
        return result

    def execute_payment(self) -> requests.Response:
        self.pre_payment_checks()

        if not self.amount:
            raise AttributeError("No Amount")

        result = self.manager.execute_payment(
            buyer=self.buyer,
            amount=self.amount,
            redirect_urls=self.redirect_urls,
            token=self.token,
        )

        return result

    def get_payment(self, payment_id: str) -> requests.Response:
        return self.manager.get_payment(payment_id)

    def register_customer(self):
        if not self.buyer:
            raise AttributeError("No Customer/Buyer set")

        result = self.manager.register_customer(customer=self.buyer)
        if result.status_code == 200:
            self.buyer.customer_id = result.json().get("id")
        return result

    def get_customer(self, customer_id: str) -> requests.Response:
        return self.manager.get_customer(customer_id)

    def update_customer(
        self, customer_id: str, fields: Dict = dict
    ) -> requests.Response:
        return self.manager.update_customer(customer_id=customer_id, fields=fields)

    def delete_customer(self, customer_id: str) -> requests.Response:
        return self.manager.delete_customer(customer_id)

    def save_card_to_vault(
        self, is_default: bool = True, redirect_urls: Dict = REDIRECT_URLS
    ):
        self.pre_payment_checks()

        return self.manager.save_card_to_vault(
            buyer=self.buyer,
            card=self.card,
            is_default=is_default,
            redirect_urls=redirect_urls,
        )

    def get_cards_in_vault(self):
        if not self.buyer:
            raise AttributeError("No Buyer/Customer set")

        return self.manager.get_cards_in_vault(buyer=self.buyer)

    def get_card_in_vault(self, card_token: str):
        if not self.buyer:
            raise AttributeError("No Buyer/Customer set")

        return self.manager.get_card_in_vault(buyer=self.buyer, card_token=card_token)

    def update_card_in_vault(self, card_token: str, fields: Dict):
        if not self.buyer:
            raise AttributeError("No Buyer/Customer set")

        return self.manager.update_card_in_vault(
            buyer=self.buyer, card_token=card_token, fields=fields
        )

    def delete_card_in_vault(self, card_token: str):
        if not self.buyer:
            raise AttributeError("No Buyer/Customer set")

        return self.manager.delete_card_in_vault(
            buyer=self.buyer, card_token=card_token
        )

    def execute_vault_payment(self) -> requests.Response:
        self.pre_payment_checks()

        if not self.amount:
            raise AttributeError("No Amount")

        result = self.manager.execute_vault_payment(
            buyer=self.buyer, amount=self.amount, card=self.card
        )

        return result
