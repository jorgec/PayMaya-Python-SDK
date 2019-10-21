import unittest

from core.payment_api_manager import PaymentAPIManager
from paymaya_sdk import PayMayaSDK
from .cards import ms_2
from .merchants import m1


class PaymentTests(unittest.TestCase):
    def test_token(self):
        paymaya = PayMayaSDK.get_instance()

        paymaya.init_payment(public_api_key=m1.public_key, secret_api_key=m1.secret_key)

        manager = PaymentAPIManager()

        result = manager.create_payment_token(card=ms_2)

        assert result.status_code == 200
