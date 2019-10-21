"""
PayMaya test API keys
Source: https://developers.paymaya.com/blog/entry/api-test-merchants-and-test-cards
"""


class Merchant:
    name: str
    secret_key: str
    public_key: str

    def __init__(self, name: str, secret: str, public: str):
        self.name = name
        self.secret_key = secret
        self.public_key = public


m1 = Merchant(
    'Sandbox Party 1',
    'sk-X8qolYjy62kIzEbr0QRK1h4b4KDVHaNcwMYk39jInSl',
    'pk-Z0OSzLvIcOI2UIvDhdTGVVfRSSeiGStnceqwUE7n0Ah'
)

m2 = Merchant(
    'Sandbox Party 2',
    'sk-KfmfLJXFdV5t1inYN8lIOwSrueC1G27SCAklBqYCdrU',
    'pk-eo4sL393CWU5KmveJUaW8V730TTei2zY8zE4dHJDxkF'
)
