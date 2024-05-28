from cryptography.hazmat.primitives.asymmetric import ed25519
from urllib.parse import urlparse, urlencode
import urllib
import json
import requests

class API:
    def __init__(self, secret_key: str, api_key: str):
        self.secret_key = secret_key
        self.api_key = api_key
        self.base_url = "https://coinswitch.co"
        self.headers = {
            "Content-Type": "application/json"
        }

    def call_api(self, url: str, method: str, headers: dict = None, payload: dict = {}):
        final_headers = self.headers.copy()
        if headers is not None:
            final_headers.update(headers)

        response = requests.request(method, url, headers=final_headers, json=payload)
        if response.status_code == 429:
            print("Rate limiting in effect.")
        return response.json()

    def signature_message(self, method: str, url: str, payload: dict):
        message = method + url + json.dumps(payload, separators=(',', ':'), sort_keys=True)
        return message

    def get_signature_of_request(self, secret_key: str, request_string: str) -> str:
        try:
            request_string = bytes(request_string, 'utf-8')
            secret_key_bytes = bytes.fromhex(secret_key)
            secret_key = ed25519.Ed25519PrivateKey.from_private_bytes(secret_key_bytes)
            signature_bytes = secret_key.sign(request_string)
            signature = signature_bytes.hex()
        except ValueError:
            return False
        return signature

    def make_request(self, method: str, endpoint: str, payload: dict = {}, params: dict = {}):
        decoded_endpoint = endpoint
        if method == "GET" and len(params) != 0:
            endpoint += ('&', '?')[urlparse(endpoint).query == ''] + urlencode(params)
            decoded_endpoint = urllib.parse.unquote_plus(endpoint)

        signature_msg = self.signature_message(method, decoded_endpoint, payload)
        signature = self.get_signature_of_request(self.secret_key, signature_msg)
        if not signature:
            return {"message": "Please Enter Valid Keys"}

        headers = {
            "X-AUTH-SIGNATURE": signature,
            "X-AUTH-APIKEY": self.api_key
        }

        url = f"{self.base_url}{endpoint}"
        response = self.call_api(url, method, headers=headers, payload=payload)
        return response

    def remove_trailing_zeros(self, dictionary):
        for key, value in dictionary.items():
            if isinstance(value, (int, float)) and dictionary[key] == int(dictionary[key]):
                dictionary[key] = int(dictionary[key])
        return dictionary

    def check_connection(self):
        return self.make_request("GET", "/api-trading-service/api/v1/validate/keys")
    
    def check_ping(self):
        return self.make_request("GET", "/trade/api/v2/ping")

    def create_order(self, payload: dict = {}):
        payload = self.remove_trailing_zeros(payload)
        return self.make_request("POST", "/trade/api/v2/order", payload=payload)

    def get_user_portfolio(self):
        return self.make_request("GET", "/trade/api/v2/user/portfolio")
