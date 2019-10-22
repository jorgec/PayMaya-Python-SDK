import json
from decimal import Decimal


class AmountModel:
    total: Decimal
    currency_code: str

    def __init__(self, *, total: Decimal = 0.0, currency_code: str = "PHP"):
        self.total = round(total, 2)
        self.currency_code = currency_code

    def as_dict(self):
        data = {"amount": str(self.total), "currency": self.currency_code}

        return data

    def serialize(self):
        return json.dumps(self.as_dict())


class TotalAmountDetailModel:
    discount: Decimal
    service_charge: Decimal
    shipping_fee: Decimal
    tax: Decimal
    subtotal: Decimal

    def __init__(self):
        self.discount = Decimal(0)
        self.service_charge = Decimal(0)
        self.shipping_fee = Decimal(0)
        self.tax = Decimal(0)
        self.subtotal = Decimal(0)

    def as_dict(self):
        data = {
            "discount": str(self.discount),
            "serviceCharge": str(self.service_charge),
            "shippingFee": str(self.shipping_fee),
            "tax": str(self.tax),
            "subtotal": str(self.subtotal),
        }
        return data

    def serialize(self):
        return json.dumps(self.as_dict())


class TotalAmountModel:
    amount: AmountModel
    details: TotalAmountDetailModel

    def as_dict(self):
        data = {
            "totalAmount": {
                "currency": self.amount.currency_code,
                "value": self.amount.total,
                "details": self.details.as_dict(),
            }
        }
        return data

    def serialize(self):
        return json.dumps(self.as_dict())
