import os
from lib.api import API
from lib.alert import send_order_alert, send_notification_alert

# Authentication keys
SECRETKEY = os.environ.get('SECRETKEY')
APIKEY = os.environ.get('APIKEY')

# Create API Object
api_connector = API(SECRETKEY, APIKEY)

user_portfolio = api_connector.get_user_portfolio()

def get_main_balance():
    for data in user_portfolio['data']:
        if data['currency'] == 'INR':
            return float(data['main_balance'])
    return 0.0

def find_coin(coin_name):
    for data in user_portfolio['data']:
        if data['currency'] == coin_name:
            return True
    return False

def ticker(coin_name):
    params = {
        "symbol": coin_name,
        "exchange": "coinswitchx"
    }
    ticker = api_connector.ticker(params=params)
    price = round(float(ticker['data']['coinswitchx']['lastPrice']), 4)
    return price

def get_coin_quantity(coin_name):
    for data in user_portfolio['data']:
        if data['currency'] == coin_name:
            return float(data['main_balance'])
    return 0.0


def place_order(side, symbol, result_1d, result_1w, b1_1d, b2_1d, b1_1w, b2_1w, h1_1d, h2_1d, h1_1w, h2_1w):
    coin_name = symbol.split('/')[0]  # Convert coin name e.g. BTC/INR => BTC
    balance = get_main_balance()  # Get fund or main balance from portfolio
    coin_exists = find_coin(coin_name)  # Check the coin exists in portfolio or not
    price = ticker(symbol)  # Get current price of crypto
    
    if side == 'buy':
        buy_quantity = 100 / price  # Calculate buy quantity (Note: Always invest 100 INR from portfolio balance)
        if balance >= 110:
            payload = {
                "side": side,
                "symbol": symbol,
                "type": "limit",
                "price": price + 0.5,  # Adding a small buffer to the price
                "quantity": buy_quantity,
                "exchange": "coinswitchx"
            }
            response = api_connector.create_order(payload=payload)
            send_order_alert(response)
        else:
            error = 'Insufficient funds for trade! Please add more than 200 INR'
            send_notification_alert('Buy', symbol, price, result_1d, result_1w, b1_1d, b2_1d, b1_1w, b2_1w, h1_1d, h2_1d, h1_1w, h2_1w, error)
    
    elif side == 'sell':
        sell_quantity = get_coin_quantity(coin_name)  # Get coin quantity from portfolio
        if coin_exists and sell_quantity > 0:
            payload = {
                "side": side,
                "symbol": symbol,
                "type": "limit",
                "price": price - 0.5,  # Subtracting a small buffer from the price
                "quantity": sell_quantity,
                "exchange": "coinswitchx"
            }
            response = api_connector.create_order(payload=payload)
            if response.get("status") == "success":
                send_order_alert(side, symbol, price, sell_quantity, balance)
            else:
                send_alert(f"Sell Order failed: {response.get('message', 'Unknown error')}")
                