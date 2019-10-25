import datetime
import json

# CC Types
MASTERCARD = "MasterCard"
VISA = "Visa"


class CardModel:
    card_type: str
    number: str
    expiry_month: str
    expiry_year: str
    cvc: str
    password: str
    token: str = None
    token_state: str = None

    def __init__(
        self,
        *,
        number: str,
        expiry_month: str,
        expiry_year: str,
        cvc: str,
        card_type: str,
        password: str = None,
    ):

        if self.validate_cvc(cvc):
            self.cvc = cvc
        else:
            raise ValueError("CVC is invalid")

        if self.validate_month(expiry_month):
            self.expiry_month = expiry_month
        else:
            raise ValueError(f"Expiry Month is invalid: {expiry_month}")

        if self.validate_year(expiry_year):
            self.expiry_year = expiry_year
        else:
            raise ValueError("Expiry Year is invalid")

        self.number = number
        self.card_type = card_type
        self.password = password

    def __str__(self):
        pad = "X" * (len(self.number) - 6)
        return f"{self.number[:3]}{pad}{self.number[-3:]}"

    @staticmethod
    def validate_cvc(cvc: str) -> bool:
        try:
            int(cvc)
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_month(m: str) -> bool:
        try:
            month = int(m)
            if 1 <= month <= 12:
                return True
            return False
        except ValueError:
            return False

    @staticmethod
    def validate_year(y: str) -> bool:
        try:
            year = int(y)
            if (
                year < datetime.datetime.now().year
                or year > datetime.datetime.now().year + 20
            ):
                return False
            return True
        except ValueError:
            return False

    def as_dict(self):
        data = {
            "number": self.number,
            "cvc": self.cvc,
            "expMonth": self.expiry_month,
            "expYear": self.expiry_year,
        }

        return data

    def serialize(self):
        return json.dumps({"card": self.as_dict()})
