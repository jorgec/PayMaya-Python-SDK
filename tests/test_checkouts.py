import decimal
import random
import unittest

import dumper
from faker import Faker

from models.amount_models import AmountModel, TotalAmountModel
from models.buyer_models import BuyerModel
from models.checkout_data_models import CheckoutDataModel
from models.checkout_item_models import CheckoutItemModel
from paymaya_sdk import PayMayaSDK
from .merchants import m1

fake = Faker()


class CheckoutTests(unittest.TestCase):
    def test_checkout(self):
        paymaya = PayMayaSDK()
        paymaya.set_keys(
            public_api_key=m1.public_key,
            secret_api_key=m1.secret_key,
        )

        checkout = paymaya.checkout('cGstZW80c0wzOTNDV1U1S212ZUpVYVc4VjczMFRUZWkyelk4ekU0ZEhKRHhrRjo=')

        amt = decimal.Decimal(random.uniform(100, 500))
        amount = AmountModel(total=amt, currency_code="PHP")
        single_amount = TotalAmountModel(amount=amount)

        profile = fake.profile()
        buyer = BuyerModel(
            first_name=profile.get("name").split(" ")[0],
            last_name=profile.get("name").split(" ")[-1],
        )
        item = CheckoutItemModel()
        item.name = fake.name()
        item.code = fake.uuid4()
        item.quantity = fake.random_int(1, 10)
        item.amount = single_amount
        total_amount = TotalAmountModel(
            amount=AmountModel(
                total=item.quantity * amount.total,
                currency_code='PHP'
            )
        )
        item.total_amount = total_amount

        checkout_data = CheckoutDataModel()
        checkout_data.total_amount = total_amount
        checkout_data.buyer = buyer
        checkout_data.items = [item.as_dict()]
        checkout_data.request_reference_number = fake.uuid4()

        checkout.initiate(checkout_data)

        result = checkout.execute()

        assert result, dumper.dump(checkout)
