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
