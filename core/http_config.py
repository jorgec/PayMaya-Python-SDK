from typing import Dict

HEADER_SEPARATOR = ";"
HTTP_GET = "GET"
HTTP_POST = "POST"
HTTP_PUT = "PUT"
HTTP_DELETE = "DELETE"


class HTTPConfig:
    url: str = ""
    headers: Dict = {"Content-Type": "application/json"}
    method: str = ""

    def __init__(
        self, *, url: str = None, method: str = HTTP_POST, headers: Dict = dict
    ):
        self.url = url
        self.method = method
        self.headers = {**self.headers, **headers}
