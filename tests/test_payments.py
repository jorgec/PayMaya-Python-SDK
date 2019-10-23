import decimal
import random
import unittest

from faker import Faker

from models.amount_models import AmountModel
from models.buyer_models import BuyerModel
from paymaya_sdk import PayMayaSDK
from .cards import ms_2
from .merchants import m1

fake = Faker()


class PaymentTests(unittest.TestCase):
    def test_token(self):
        paymaya = PayMayaSDK()
        paymaya.set_keys(
            public_api_key=m1.public_key,
            secret_api_key=m1.secret_key,
        )

        payment = paymaya.payment()
        payment.card = ms_2

        token_result = payment.create_token()

        assert token_result

    def test_payment(self):
        paymaya = PayMayaSDK()
        paymaya.set_keys(
            public_api_key=m1.public_key,
            secret_api_key=m1.secret_key,
        )

        payment = paymaya.payment()
        payment.card = ms_2

        payment.create_token()

        amt = decimal.Decimal(random.uniform(100, 10000))
        amount = AmountModel(total=amt, currency_code="PHP")

        profile = fake.profile()
        buyer = BuyerModel(
            first_name=profile.get("name").split(" ")[0],
            last_name=profile.get("name").split(" ")[-1],
        )

        payment.buyer = buyer
        payment.amount = amount
        payment_result = payment.execute_payment()

        assert payment_result

        assert payment.manager.payments
