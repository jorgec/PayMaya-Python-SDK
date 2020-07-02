from core.api_manager import APIManager
from core.constants import PRODUCTION, PAYMENTS_PRODUCTION_URL, PAYMENTS_SANDBOX_URL


class PaymentAPIManager(APIManager):
    base_url: str = None

    def __init__(self, *args, **kwargs):
        self.base_url = self.get_base_url()
        super().__init__(*args, **kwargs)

    def get_base_url(self) -> str:
        if self.environment == PRODUCTION:
            url = PAYMENTS_PRODUCTION_URL
        else:
            url = PAYMENTS_SANDBOX_URL

        return url
