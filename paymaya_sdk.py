"""
MIT License

Copyright (c) 2019 Jorge Cosgayon

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
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
