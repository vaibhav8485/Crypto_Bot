# STD Modules
from cryptography.hazmat.primitives.asymmetric import ed25519
from urllib.parse import urlparse, urlencode
import urllib
import json
import requests
import os
import logging

# User Define Modules
from lib.risk import load_log_file, update_log_file

# Basic configuration for logging
logging.basicConfig(level=logging.INFO)

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
    
    def get_user_portfolio(self):
        return self.make_request("GET", "/trade/api/v2/user/portfolio")
    
    def ticker(self, params: dict = {}):
        return self.make_request("GET", "/trade/api/v2/24hr/ticker", params=params)

    def create_order(self, payload: dict = {}):
        payload = self.remove_trailing_zeros(payload)
        return self.make_request("POST", "/trade/api/v2/order", payload=payload)

# Authentication Credential
SECRETKEY = os.environ.get('SECRETKEY')
APIKEY = os.environ.get('APIKEY')

# Create API Obj
api_connector = API(SECRETKEY, APIKEY)

# Get Portfolio Information
user_portfolio = api_connector.get_user_portfolio()

# Get INR Balance
def get_main_balance():
    for data in user_portfolio['data']:
        if data['currency'] == 'INR':
            return float(data['main_balance'])
    return 0.0

# Find Crypto Function
def find_coin(symbol):
    crypto_name = symbol.split('/')[0]
    for data in user_portfolio['data']:
        if data['currency'] == crypto_name:
            return True
    return False

# Get Current Price of Crypto
def ticker(coin_name):
    params = {
        "symbol": coin_name,
        "exchange": "coinswitchx"
    }
    ticker = api_connector.ticker(params=params)
    price = round(float(ticker['data']['coinswitchx']['lastPrice']), 4)
    return price

# Get Crypto Quantity
def get_coin_quantity(symbol):
    crypto_name = symbol.split('/')[0]
    for data in user_portfolio['data']:
        if data['currency'] == crypto_name:
            return float(data['main_balance'])
    return 0.0

# Get Crypto Count that Not Exists
def get_investment_amount():
    # Crypto Watch list (12 Assets)
    watchlist = ["BTC/INR", "ETH/INR", "MATIC/INR", "XRP/INR", "ADA/INR", "BAT/INR", "BNB/INR", "SOL/INR", "NEAR/INR", "SAND/INR", "DOGE/INR", "STX/INR"]
    count = 0 # Set Count 0 Default
    for symbol in watchlist:
        coin_exists = find_coin(symbol)
        if coin_exists == False:
            count += 1

    balance = get_main_balance()
    amount = balance / count

    # Return quantity
    return int(amount)

# Place Buy Order
def buy_order(symbol):
    try:
        price = ticker(symbol) # Get Current Price
        buy_amount = get_investment_amount() # Get Crypto Count
        buy_quantity = round(float(buy_amount / price), 4) # Cal Buy Quantity
        payload = {
            "side": "buy",
            "symbol": symbol,
            "type": "limit",
            "price": price + 1,  # Adding a small buffer to the price
            "quantity": buy_quantity,
            "exchange": "coinswitchx"
        }
        response = api_connector.create_order(payload=payload)

        file_path = "log.json" # Log File Name
        log = load_log_file(file_path) # Load JSON File
        print("Log Data Inside Buy Order:", log)

        if log:     
            # Update Buy Buy Log.JSON
            update_log_file(file_path, symbol, price, 'auto')

            # Return Buy Order Response
            return response
        else:
            print(f"File '{file_path}' does not exist or is empty.")
    except Exception as e:
        logging.error(f"An unexpected error occurred in Buy Order: {e}")

# Place Sell Order
def sell_order(symbol):
    try:
        price = ticker(symbol) # Get Current Crypto Price
        sell_quantity = get_coin_quantity(symbol) # Get Quantity
        payload = {
            "side": "sell",
            "symbol": symbol,
            "type": "limit",
            "price": price - 1,  # Subtracting a small buffer from the price
            "quantity": sell_quantity,
            "exchange": "coinswitchx"
        }
        response = api_connector.create_order(payload=payload)
        # Return Sell Order Response
        return response
    except Exception as e:
        logging.error(f"An unexpected error occurred in Sell Order: {e}")
