import json


class BuyerAddress:
    address1: str
    address2: str
    city: str
    state: str
    zip_code: str
    country: str

    def __init__(
        self,
        *,
        address1: str = "",
        address2: str = "",
        city: str = "",
        state: str = "",
        zip_code: str = "",
        country: str = "PH",
    ):
        self.address1 = address1
        self.address2 = address2
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.country = country

    def __str__(self):
        return f"{self.address1} {self.address2} {self.city}"

    def as_dict(self):
        data = {
            "line1": self.address1,
            "line2": self.address2,
            "city": self.city,
            "state": self.state,
            "zipCode": self.zip_code,
            "countryCode": self.country,
        }
        return data

    def serialize(self):
        return json.dumps(self.as_dict())


class BuyerContact:
    phone: str
    email: str

    def __init__(self, *, phone: str = "", email: str = ""):
        self.phone = phone
        self.email = email

    def as_dict(self):
        data = {"phone": self.phone, "email": self.email}
        return data

    def serialize(self):
        return json.dumps(self.as_dict())


class BuyerModel:
    first_name: str
    middle_name: str
    last_name: str
    contact: BuyerContact
    billing_address: BuyerAddress
    shipping_address: BuyerAddress
    ip_address: str

    def __init__(
        self, *, first_name: str = "", middle_name: str = "", last_name: str = ""
    ):
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.contact = BuyerContact()
        self.billing_address = BuyerAddress()
        self.shipping_address = BuyerAddress()
        self.ip_address = "0.0.0.0"

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"

    def as_dict(self):
        data = {
            "firstName": self.first_name,
            "middleName": self.middle_name,
            "lastName": self.last_name,
            "contact": self.contact.as_dict(),
            "billingAddress": self.billing_address.as_dict(),
            "shippingAddress": self.shipping_address.as_dict(),
            "ipAddress": self.ip_address,
        }

        return data

    def serialize(self):
        return json.dumps(self.as_dict())
