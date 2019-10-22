from typing import Dict, List

from core.constants import REDIRECT_URLS
from core.payment_api_manager import PaymentAPIManager
from models.amount_model import AmountModel
from models.buyer_model import BuyerModel
from models.card_model import CardModel


class PaymentAPI:
    token: str = None
    amount: AmountModel = None
    buyer: BuyerModel = None
    __card: CardModel = None
    redirect_urls: Dict = None

    manager: PaymentAPIManager

    @property
    def card(self) -> CardModel:
        return self.__card

    @card.setter
    def card(self, card: CardModel):
        self.__card = card
        self.token = ""
        self.manager = PaymentAPIManager()

    def __init__(self):
        self.token = ""
        self.manager = PaymentAPIManager()

    def create_token(self) -> bool:
        if not self.card:
            raise ValueError("No card registered")

        result = self.manager.create_payment_token(card=self.card)
        if result:
            self.token = self.manager.token
            return True
        return False

    def execute_payment(self) -> bool:
        if not self.token:
            raise AttributeError("No Token")

        if not self.buyer:
            raise AttributeError("No Buyer")

        if not self.amount:
            raise AttributeError("No Amount")

        if not self.redirect_urls:
            self.redirect_urls = REDIRECT_URLS

        result = self.manager.charge_card(
            buyer=self.buyer, amount=self.amount, redirect_urls=self.redirect_urls
        )

        return result

    def payments(self) -> List:
        return self.manager.payments

    def query_payment(self, payment_id: str) -> Dict:
        return self.manager.query_payment(payment_id)
