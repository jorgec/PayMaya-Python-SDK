import json

from models.amount_models import TotalAmountModel


class CheckoutItemModel:
    name: str
    code: str
    description: str
    quantity: int
    amount: TotalAmountModel
    total_amount: TotalAmountModel

    def __init__(self):
        self.name = ''
        self.code = ''
        self.description = ''
        self.quantity = 0
        self.amount = TotalAmountModel()
        self.total_amount = TotalAmountModel()

    def __str__(self):
        return f'{self.name}'

    def as_dict(self):
        data = {
            "name": self.name,
            "code": self.code,
            "description": self.description,
            "quantity": self.quantity,
            "amount": self.amount.as_dict(),
            "totalAmount": self.total_amount.as_dict()
        }

        return data

    def serialize(self):
        return json.dumps(self.as_dict())
