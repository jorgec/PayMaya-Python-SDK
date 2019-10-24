# Unofficial PayMaya-Python-SDK
This SDK allows Python applications to accept payments from MasterCard/Visa cardholders via the <a href="https://developers.paymaya.com/blog/entry/paymaya-api-and-sdk-documentation">PayMaya API</a>. Tested on Python 3.6, 3.7, and 3.8

I've tried to pattern the flow on the existing PayMaya SDK libraries as much as possible (ref: <a href="https://github.com/PayMaya/PayMaya-PHP-SDK/">PayMaya PHP SDK</a>) 

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Build Status](https://travis-ci.com/jorgec/PayMaya-Python-SDK.svg?branch=master)](https://travis-ci.com/jorgec/PayMaya-Python-SDK)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)
[![codecov](https://codecov.io/gh/jorgec/PayMaya-Python-SDK/branch/master/graph/badge.svg)](https://codecov.io/gh/jorgec/PayMaya-Python-SDK)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
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
### Models
The data models have 2 convenience functions: `as_dict()` and `serialize()`:
- `as_dict()` returns a Dict with keys matching the ones expected by the PayMaya API, and converting all data into JSON-safe types (str mostly)
- `serialize()` returns a JSON dump of `as_dict()`
### Payments
#### 1. Import the SDK and the API libraries
```python
from paymaya_sdk import PayMayaSDK
from api.payment_api import PaymentAPI
from models.amount_model import AmountModel
from models.buyer_model import BuyerModel
from models.card_model import CardModel

# for amounts
from decimal import Decimal
```
#### 2. Initialize SDK with public-facing API key, secret API key, and the intended environment ("SANDBOX" or "PRODUCTION)
```python
paymaya = PayMayaSDK()
paymaya.set_keys(
    public_api_key=<PUBLIC_KEY>,
    secret_api_key=<SECRET_KEY>,
    environment=<"SANDBOX/PRODUCTION">
)
```
#### 3. Initialize the payment object:
```python
payment = paymaya.payment()
```
#### 4. Create the Card object and tokenize it
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
#### 5. Create the Buyer and Amount objects, and execute a payment
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
#### 6. Check payments executed:
```python
# returns a list of dictionaries with the json responses
payment.payments()
```
#### 7. Query payments
```python
payment.query_payment(payment_id=<uuid>)
```
### Checkouts
```python
from models.amount_models import AmountModel, TotalAmountModel
from models.buyer_models import BuyerModel
from models.checkout_data_models import CheckoutDataModel
from models.checkout_item_models import CheckoutItemModel
from paymaya_sdk import PayMayaSDK

paymaya = PayMayaSDK()

# The provided sample API keys don't seem to work for the PayMaya checkout sandbox, 
# but this encoded string from their docs does: 
# https://s3-us-west-2.amazonaws.com/developers.paymaya.com.pg/checkout/checkout.html 
# so I provided a parameter to override the keys as needed, for testing
paymaya.set_keys(
    public_api_key=<PUBLIC_KEY>,
    secret_api_key=<SECRET_KEY>,
    environment=<"SANDBOX/PRODUCTION">,
    encoded_key='cGstZW80c0wzOTNDV1U1S212ZUpVYVc4VjczMFRUZWkyelk4ekU0ZEhKRHhrRjo='
)
checkout = paymaya.checkout()

buyer = BuyerModel(
    first_name="Juan",
    last_name="Dela Cruz",
)
item = CheckoutItemModel()
item.name = "Crispy Pata"
item.code = "FOOD-CP"
item.quantity = "1"
item.amount = Amount(total=Decimal(200), currency_code='PHP')
item.total_amount = TotalAmountModel(
    amount=AmountModel(
        total=int(item.quantity) * item.amount.total,
        currency_code=item.amount.curency_code
    )
)

checkout_data = CheckoutDataModel()
checkout_data.total_amount = item.total_amount
checkout_data.buyer = buyer
checkout_data.items = [item.as_dict()]
checkout_data.request_reference_number = "REF-MERCHANT-GENERATED"

# optionally:
# checkout_data.redirect_urls = {
#     "success": "http://www.askthemaya.com/",
#     "failure": "http://www.askthemaya.com/failure?id=6319921",
#     "cancel": "http://www.askthemaya.com/cancel?id=6319921"
# }
# and
# checkout_data.metadata = {...}

checkout.initiate(checkout_data)

result = checkout.execute()
```
## Summary/Changelog
2019-10-23
Checkout functionality
Trying out non-Singleton implementation

2019-10-22: 
Payment functionality is available for:
- creating tokens
- executing payments
- querying payments