import json


class CheckoutCustomizationModel:
    logo_url: str = None
    icon_url: str = None
    apple_touch_icon_url: str = None
    custom_title: str = None
    color_scheme: str = None

    def __init__(self, *args, **kwargs):
        self.logo_url = kwargs.get("logo_url", None)
        self.icon_url = kwargs.get("icon_url", None)
        self.apple_touch_icon_url = kwargs.get("apple_touch_icon_url", None)
        self.custom_title = kwargs.get("custom_title", None)
        self.color_scheme = kwargs.get("color_scheme", None)

    def as_dict(self):
        data = {
            "logoUrl": self.logo_url,
            "iconUrl": self.icon_url,
            "appleTouchIconUrl": self.apple_touch_icon_url,
            "customTitle": self.custom_title,
            "colorScheme": self.color_scheme,
        }

        return data

    def serialize(self):
        return json.dumps({"card": self.as_dict()})
