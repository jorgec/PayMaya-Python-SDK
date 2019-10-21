from payment.sdks.paymaya.models.card import Card


class Payment:
    card: Card

    def __init__(self, card: Card):
        self.card = card
