import unittest
from paymaya_sdk import PayMayaSDK
from .merchants import m1
from faker import Faker

fake = Faker()


class WebhookTests(unittest.TestCase):
    def test_create_webhook(self):
        paymaya = PayMayaSDK()
        paymaya.set_keys(
            public_api_key=m1.public_key,
            secret_api_key=m1.secret_key,
            encoded_key="cGstZW80c0wzOTNDV1U1S212ZUpVYVc4VjczMFRUZWkyelk4ekU0ZEhKRHhrRjo=",
        )

        checkout = paymaya.checkout()

        result = checkout.register_webhook(name="TEST_WEBHOOK", callback_url="http://localhost/callback")

        json_result = result.json()

        assert result.status_code == 200
        assert json_result["name"] == "TEST_WEBHOOK"
        assert json_result["callbackUrk"] == "http://localhost/callback"
