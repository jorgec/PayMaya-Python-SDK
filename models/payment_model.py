import json
from typing import Dict

from core.constants import REDIRECT_URLS
from .amount_model import AmountModel
from .buyer_model import BuyerModel


class PaymentModel:
    token: str
    amount: AmountModel
    buyer: BuyerModel
    redirect_urls: Dict

    def __init__(
        self, *, token: str, buyer: BuyerModel, amount: AmountModel, urls: Dict = REDIRECT_URLS
    ):
        self.token = token
        self.amount = amount
        self.buyer = buyer
        self.redirect_urls = urls

    def as_dict(self):
        data = {
            "paymentTokenId": self.token,
            "totalAmount": self.amount.as_dict(),
            "buyer": self.buyer.as_dict(),
            "redirectUrl": self.redirect_urls,
        }

        return data

    def serialize(self):
        return json.dumps(self.as_dict())
