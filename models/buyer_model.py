import json


class BuyerModel:
    first_name: str
    middle_name: str
    last_name: str
    phone: str
    email: str
    address1: str
    address2: str
    city: str
    state: str
    zip_code: str
    country: str

    def __init__(
        self,
        *,
        first_name: str = "",
        middle_name: str = "",
        last_name: str = "",
        phone: str = "",
        email: str = "",
        address1: str = "",
        address2: str = "",
        city: str = "",
        state: str = "",
        zip_code: str = "",
        country: str = "PH",
    ):
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.address1 = address1
        self.address2 = address2
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.country = country

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"

    def as_dict(self):
        data = {
            "firstName": self.first_name,
            "middleName": self.middle_name,
            "lastName": self.last_name,
            "contact": {"phone": self.phone, "email": self.email},
            "billingAddress": {
                "line1": self.address1,
                "line2": self.address2,
                "city": self.city,
                "state": self.state,
                "zipCode": self.zip_code,
                "countryCode": self.country,
            },
        }

        return data

    def serialize(self):
        return json.dumps(self.as_dict())
