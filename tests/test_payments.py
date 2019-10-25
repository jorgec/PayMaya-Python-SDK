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
        paymaya.set_keys(public_api_key=m1.public_key, secret_api_key=m1.secret_key)

        payment = paymaya.payment()
        payment.card = ms_2

        token_result = payment.create_token()

        assert token_result, print(token_result.json())

    def test_payment(self):
        paymaya = PayMayaSDK()
        paymaya.set_keys(public_api_key=m1.public_key, secret_api_key=m1.secret_key)

        payment = paymaya.payment()

        amt = decimal.Decimal(random.uniform(100, 10000))
        amount = AmountModel(total=amt, currency_code="PHP")

        profile = fake.profile()
        buyer = BuyerModel(
            first_name=profile.get("name").split(" ")[0],
            last_name=profile.get("name").split(" ")[-1],
        )

        payment.buyer = buyer
        payment.amount = amount
        payment.card = ms_2
        payment.create_token()
        payment_result = payment.execute_payment()

        assert payment_result.status_code == 200, print(payment_result.json())

        payment_id = payment_result.json().get("id", None)
        assert payment_id is not None, print(payment_result.json())

    def test_customer(self):
        paymaya = PayMayaSDK()
        paymaya.set_keys(public_api_key=m1.public_key, secret_api_key=m1.secret_key)

        payment = paymaya.payment()

        profile = fake.profile()
        payment.buyer = BuyerModel(
            first_name=profile.get("name").split(" ")[0],
            last_name=profile.get("name").split(" ")[-1],
        )

        customer_result = payment.register_customer()

        assert customer_result.status_code == 200, customer_result.json()

        customer_id = customer_result.json().get("id", None)
        assert customer_id is not None, print(customer_result.json())

        query_customer = payment.get_customer(customer_id=customer_id)
        assert query_customer.status_code == 200, print(query_customer.json())

        update_customer = payment.update_customer(
            customer_id=customer_id, fields={"firstName": "Macaluluoy"}
        )
        assert update_customer.status_code == 200, print(update_customer.json())
        query_customer = payment.get_customer(customer_id=customer_id)
        assert query_customer.json().get("firstName") == "Macaluluoy", print(
            query_customer.json()
        )

        payment.card = ms_2
        card_vault = payment.save_card_to_vault()

        assert card_vault.status_code == 200, print(card_vault.json())

        cards_in_vault = payment.get_cards_in_vault()
        assert cards_in_vault.status_code == 200, print(cards_in_vault.json())
        assert len(cards_in_vault.json()) == 1, print(cards_in_vault.json())
        assert cards_in_vault.json()[0].get("cardTokenId") == payment.token, print(
            cards_in_vault.json()
        )

        card_in_vault = payment.get_card_in_vault(card_token=payment.token)
        assert card_in_vault.status_code == 200, print(card_in_vault.json())
        assert card_in_vault.json().get("cardTokenId") == payment.token, print(
            card_in_vault.json()
        )

        # Updates keep failing with error: PY0026	Failed to update card details
        # Generic error for failed update of card. PayMaya issue?
        # update_card = payment.update_card_in_vault(card_token=payment.token, fields={"isDefault": False})
        # assert update_card.status_code == 200, print(update_card.json())
        #
        # card_in_vault = payment.get_card_in_vault(card_token=payment.token)
        # assert card_in_vault.status_code == 200, print(card_in_vault.json())
        # assert card_in_vault.json().get('isDefault') is False, print(card_in_vault.json())

        delete_card = payment.delete_card_in_vault(card_token=payment.token)
        assert delete_card.status_code == 200, print(delete_card.json())

        cards_in_vault = payment.get_cards_in_vault()
        # Should return "No card found for customer"
        assert cards_in_vault.status_code == 400, print(cards_in_vault.json())

        delete_customer = payment.delete_customer(customer_id)
        assert delete_customer.status_code == 200, print(delete_customer.json())
