#STD Modules
import os
from lib.api import API
from lib.alert import send_order_alert, send_notification_alert

# Authentication
SECRETKEY = os.environ.get('SECRETKEY')
APIKEY = os.environ.get('APIKEY')

# Create API Obj
api_connector = API(SECRETKEY, APIKEY)

# Create API Obj
user_portfolio = api_connector.get_user_portfolio()

# Get Balance Function
def get_main_balance():
    for data in user_portfolio['data']:
        if data['currency'] == 'INR':
            return float(data['main_balance'])
    return 0.0

# Find Crypto Function
def find_coin(coin_name):
    for data in user_portfolio['data']:
        if data['currency'] == coin_name:
            return True
    return False

# Get Current Price Function
def ticker(coin_name):
    params = {
        "symbol": coin_name,
        "exchange": "coinswitchx"
    }
    ticker = api_connector.ticker(params=params)
    price = round(float(ticker['data']['coinswitchx']['lastPrice']), 4)
    return price

# Get Crypto Quantity
def get_coin_quantity(coin_name):
    for data in user_portfolio['data']:
        if data['currency'] == coin_name:
            return float(data['main_balance'])
    return 0.0

# Main Function
def place_order(side, symbol, result_1d, result_1w, b1_1d, b2_1d, b1_1w, b2_1w, h1_1d, h2_1d, h1_1w, h2_1w):
    coin_name = symbol.split('/')[0]  # Convert coin name e.g. BTC/INR => BTC
    balance = get_main_balance()  # Get fund or main balance from portfolio
    coin_exists = find_coin(coin_name)  # Check the coin exists in portfolio or not
    price = ticker(symbol)  # Get current price of crypto
    
    if side == 'buy':
        buy_quantity = round(float(200 / price), 2)  # Calculate buy quantity (Invest 200 INR, keeping some buffer)
        if balance >= 210 and coin_exists == False:
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
            if coin_exists == False:
                error = 'Insufficient funds for trade [Mini: 210 INR]'
            else:
                error = f'You already have {coin_name}'
            send_notification_alert('Buy', symbol, price, result_1d, result_1w, b1_1d, b2_1d, b1_1w, b2_1w, h1_1d, h2_1d, h1_1w, h2_1w, error)
    
    elif side == 'sell':
        sell_quantity = get_coin_quantity(coin_name)  # Get coin quantity from portfolio
        if sell_quantity > 0 and coin_exists == True:
            payload = {
                "side": side,
                "symbol": symbol,
                "type": "limit",
                "price": price - 0.5,  # Subtracting a small buffer from the price
                "quantity": sell_quantity,
                "exchange": "coinswitchx"
            }
            response = api_connector.create_order(payload=payload)
            send_order_alert(response)
        else:
            error = f'You not have {coin_name} for Sell'
            send_notification_alert('Sell', symbol, price, result_1d, result_1w, b1_1d, b2_1d, b1_1w, b2_1w, h1_1d, h2_1d, h1_1w, h2_1w, error)
            