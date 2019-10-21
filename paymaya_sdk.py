from singleton import Singleton


class PayMayaSDK(metaclass=Singleton):
    instance = None
    checkout_public_api_key: str
    checkout_secret_api_key: str
    checkout_environment: str
    payments_public_api_key: str
    payments_secret_api_key: str
    payments_environment: str

    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            cls.instance = PayMayaSDK()
        return cls.instance

    def init_checkout(
        self,
        public_api_key: str = None,
        secret_api_key: str = None,
        environment: str = "SANDBOX",
    ):
        self.checkout_public_api_key = public_api_key
        self.checkout_secret_api_key = secret_api_key
        self.checkout_environment = environment

    def init_payment(
        self,
        public_api_key: str = None,
        secret_api_key: str = None,
        environment: str = "SANDBOX",
    ):
        self.payments_public_api_key = public_api_key
        self.payments_secret_api_key = secret_api_key
        self.payments_environment = environment
