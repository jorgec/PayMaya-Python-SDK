# Unofficial PayMaya-Python-SDK
This SDK allows Python applications to accept payments from MasterCard/Visa cardholders via the <a href="https://developers.paymaya.com/blog/entry/paymaya-api-and-sdk-documentation">PayMaya API</a>. Tested on Python 3.6, 3.7, and 3.8

I've tried to pattern the flow on the existing PayMaya SDK libraries as much as possible (ref: <a href="https://github.com/PayMaya/PayMaya-PHP-SDK/">PayMaya PHP SDK</a>) 

[![Build Status](https://travis-ci.com/jorgec/PayMaya-Python-SDK.svg?branch=master)](https://travis-ci.com/jorgec/PayMaya-Python-SDK)
[![codecov](https://codecov.io/gh/jorgec/PayMaya-Python-SDK/branch/master/graph/badge.svg)](https://codecov.io/gh/jorgec/PayMaya-Python-SDK)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Prerequisites
- Python 3.6+
- <a href="https://pypi.org/project/requests/">requests</a>

## Tests
- pytest

## Installation
- Clone this project

## Prerequisites

#### _API Keys_
To use PayMaya Python SDK, you need to have a different API key for Sandbox and Production environment.
 
##### _Sandbox Environment_
 
Sandbox credentials are useful for testing application integration. All transactions and money flow made in this environment are only simulated and does not reflect your production records. The following sandbox API key can be used for testing purposes:

 ```
Public-facing API Key: pk-iaioBC2pbY6d3BVRSebsJxghSHeJDW4n6navI7tYdrN

Secret API Key: sk-uh4ZFfx9i0rZpKN6CxJ826nVgJ4saGGVAH9Hk7WrY6Q
```
 
##### _Production Environment_
 
Upon successful integration testing, you can then request for production credentials. Upon receipt, just change your SDK initialization to use production environment to start accepting live transactions.

## Usage
1. Import the SDK and the API libraries
```python
from paymaya_sdk import PayMayaSDK
from api.payment_api import PaymentAPI
from models.amount_model import AmountModel
from models.buyer_model import BuyerModel
from models.card_model import CardModel

# for amounts
from decimal import Decimal
```
1. Initialize SDK with public-facing API key, secret API key, and the intended environment ("SANDBOX" or "PRODUCTION)
```python
PayMayaSDK.get_instance().init_payment(public_api_key=<PUBLIC_KEY>, secret_api_key=<SECRET_KEY>, environment=<"SANDBOX"/"PRODUCTION">)
```
1. Initialize the payment object:
```python
payment = PaymentAPI()
```
1. Create the Card object and tokenize it
```python
payment.card = CardModel(
    number="5123456789012346",
    expiry_month="12",
    expiry_year="2025",
    cvc="111",
    card_type="MASTERCARD",
)

payment.create_token()
```
1. Create the Buyer and Amount objects, and execute a payment
```python
payment.amount = AmountModel(total=Decimal(1000), currency_code='PHP')
payment.buyer = BuyerModel(
    first_name="Juan",
    middle_name="De La",
    last_name="Cruz",
    phone='+639171234567',
    email='randomemail@randomdomain.com',
    address1='48584 Johnson Trace Suite ',
    address2='2612 Jessica Meadow',
    city='Quezon City',
    state='Metro Manila',
    zip_code='1101',
    country='PH'
)
payment.execute_payment()
```
1. Check payments executed:
```python
# returns a list of dictionaries with the json responses
payment.payments()
```
1. Query payment
```python
payment.query_payment(payment_id=<uuid>)
```
## Summary
As of 2019-10-22, Payment functionality is available for:
- creating tokens
- executing payments
- querying payments