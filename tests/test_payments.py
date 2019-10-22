import decimal
import random
import unittest

from faker import Faker

from api.payment_api import PaymentAPI
from models.amount_model import Amount
from models.buyer_model import Buyer
from paymaya_sdk import PayMayaSDK
from .cards import ms_2
from .merchants import m1

fake = Faker()


class PaymentTests(unittest.TestCase):
    def test_token(self):
        PayMayaSDK.get_instance().init_payment(
            public_api_key=m1.public_key, secret_api_key=m1.secret_key
        )

        payment = PaymentAPI()
        payment.card = ms_2

        token_result = payment.create_token()

        assert token_result

        amt = decimal.Decimal(random.uniform(100, 10000))
        amount = Amount(total=amt, currency_code="PHP")

        profile = fake.profile()
        buyer = Buyer(
            first_name=profile.get("name").split(" ")[0],
            last_name=profile.get("name").split(" ")[-1],
            # phone=fake.phone_number(),
            email=profile.get("mail"),
            address1=fake.street_address(),
            address2=fake.secondary_address(),
            city=fake.city(),
            state=fake.state(),
            zip_code=fake.zipcode(),
            country=fake.country_code(representation="alpha-2"),
        )

        payment.buyer = buyer
        payment.amount = amount
        payment_result = payment.execute_payment()

        assert payment_result

        assert payment.manager.payments
