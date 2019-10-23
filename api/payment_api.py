from typing import Dict, List, TypeVar, Generic

from core.constants import REDIRECT_URLS
from core.payment_api_manager import PaymentAPIManager
from models.amount_models import AmountModel
from models.buyer_models import BuyerModel
from models.card_models import CardModel

PayMayaSDK = TypeVar("PayMayaSDK")


class PaymentAPI:
    amount: AmountModel = None
    buyer: BuyerModel = None
    __card: CardModel = None
    redirect_urls: Dict = None

    instance: Generic[PayMayaSDK]

    manager: PaymentAPIManager

    @property
    def token(self) -> str:
        return self.manager.token

    @token.setter
    def token(self, *args, **kwargs) -> None:
        pass

    @property
    def card(self) -> CardModel:
        return self.__card

    @card.setter
    def card(self, card: CardModel):
        self.__card = card
        self.manager = PaymentAPIManager(self.instance)

    def __init__(self, instance: Generic[PayMayaSDK]):
        self.instance = instance
        self.manager = PaymentAPIManager(instance)

    def create_token(self) -> bool:
        if not self.card:
            raise ValueError("No card registered")

        result = self.manager.create_payment_token(card=self.card)
        if result:
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

        result = self.manager.execute_payment(
            buyer=self.buyer, amount=self.amount, redirect_urls=self.redirect_urls
        )

        return result

    def payments(self) -> List:
        return self.manager.payments

    def query_payment(self, payment_id: str) -> Dict:
        return self.manager.query_payment(payment_id)
