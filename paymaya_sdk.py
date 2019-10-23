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
from api import PaymentAPI, CheckoutAPI


class PayMayaSDK:
    api = None
    public_api_key: str
    secret_api_key: str
    environment: str

    def set_keys(
        self,
        public_api_key: str = None,
        secret_api_key: str = None,
        environment: str = "SANDBOX",
    ) -> None:
        self.public_api_key = public_api_key
        self.secret_api_key = secret_api_key
        self.environment = environment

    def checkout(self, encoded_key: str = None) -> CheckoutAPI:
        self.api = CheckoutAPI(self, encoded_key)
        return self.api

    def payment(self) -> PaymentAPI:
        self.api = PaymentAPI(self)
        return self.api
