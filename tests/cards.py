"""
PayMaya test cards
Source: https://developers.paymaya.com/blog/entry/api-test-merchants-and-test-cards
"""

from models.card_models import CardModel

ms_1 = CardModel(
    number="5123456789012346",
    expiry_month="12",
    expiry_year="2025",
    cvc="111",
    card_type="MASTERCARD",
)
ms_2 = CardModel(
    number="5453010000064154",
    expiry_month="12",
    expiry_year="2025",
    cvc="111",
    card_type="MASTERCARD",
    password="secbarry1",
)
v_1 = CardModel(
    number="4123450131001381",
    expiry_month="12",
    expiry_year="2025",
    cvc="123",
    card_type="VISA",
    password="mctest1",
)
v_2 = CardModel(
    number="4123450131001522",
    expiry_month="12",
    expiry_year="2025",
    cvc="123",
    card_type="VISA",
    password="mctest1",
)
v_3 = CardModel(
    number="4123450131004443",
    expiry_month="12",
    expiry_year="2025",
    cvc="123",
    card_type="VISA",
    password="mctest1",
)
v_4 = CardModel(
    number="4123450131000508",
    expiry_month="12",
    expiry_year="2025",
    cvc="123",
    card_type="VISA",
)
