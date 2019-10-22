import json
from typing import Union, List, Dict

from core.constants import REDIRECT_URLS
from models.amount_models import TotalAmountModel
from models.buyer_models import BuyerModel
from models.checkout_item_models import CheckoutItemModel


class CheckoutDataModel:
    total_amount: TotalAmountModel
    buyer: BuyerModel
    items: Union[List, CheckoutItemModel]
    redirect_urls: Dict
    request_reference_number: str
    metadata: Dict

    def __init__(self):
        self.total_amount = TotalAmountModel()
        self.buyer = BuyerModel()
        self.items = []
        self.redirect_urls = REDIRECT_URLS
        self.request_reference_number = ""
        self.metadata = {}

    def __str__(self):
        return f'Checkout data for {self.buyer}'

    def as_dict(self) -> Dict:
        data = {
            "totalAmount": self.total_amount.as_dict(),
            "buyer": self.buyer.as_dict(),
            "items": self.items,
            "redirectUrl": self.redirect_urls,
            "requestReferenceNumber": self.request_reference_number,
            "metadata": self.metadata
        }
        return data

    def serialize(self):
        return json.dumps(self.as_dict())

    def add_item(self, item: CheckoutItemModel) -> None:
        self.items.append(item)
