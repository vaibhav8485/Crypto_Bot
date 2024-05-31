# import os
# from lib.api import API
# from lib.alert import send_order_alert, send_alert

# # Authentication keys
# secret_key = os.environ.get('SECRETKEY')
# api_key = os.environ.get('APIKEY')

# # Create API Object
# api_connector = API(secret_key, api_key)

# user_portfolio = api_connector.get_user_portfolio()

# def get_main_balance():
#     for data in user_portfolio['data']:
#         if data['currency'] == 'INR':
#             return float(data['main_balance'])
#     return 0.0

# def find_coin(coin_name):
#     for data in user_portfolio['data']:
#         if data['currency'] == coin_name:
#             return True
#     return False

# def get_coin_quantity(coin_name):
#     for data in user_portfolio['data']:
#         if data['currency'] == coin_name:
#             return float(data['main_balance'])
#     return 0.0


# def place_order(side, symbol, price):
#     coin_name = symbol.split('/')[0]  # Convert coin name e.g. BTC/INR => BTC
#     balance = get_main_balance()  # Get Fund or main balance from portfolio
#     coin_exists = find_coin(coin_name)  # Check the coin exists in portfolio or not
    
#     if side == 'buy':
#         buy_quantity = 100 / price  # Calculate buy quantity (Note: Always invest 100 INR from portfolio balance)
#         if balance >= 110:
#             payload = {
#                 "side": side,
#                 "symbol": symbol,
#                 "type": "limit",
#                 "price": price,
#                 "quantity": buy_quantity,
#                 "exchange": "coinswitchx"
#             }
#             response = api_connector.create_order(payload=payload)
#             if response.get("status") == "success":
#                 send_order_alert(side, symbol, price, buy_quantity, balance)
#             else:
#                 send_alert(f"Buy Order failed: {response.get('message', 'Unknown error')}")
#         else:
#             send_alert("Insufficient funds for trade! Please add more than 110 INR.")
    
#     elif side == 'sell' and coin_exists:
#         sell_quantity = get_coin_quantity(coin_name)  # Get coin quantity from portfolio
#         if sell_quantity > 0:
#             payload = {
#                 "side": side,
#                 "symbol": symbol,
#                 "type": "limit",
#                 "price": price,
#                 "quantity": sell_quantity,
#                 "exchange": "coinswitchx"
#             }
#             response = api_connector.create_order(payload=payload)
#             if response.get("status") == "success":
#                 send_order_alert(side, symbol, price, sell_quantity, balance)
#             else:
#                 send_alert(f"Sell Order failed: {response.get('message', 'Unknown error')}")












import os
from lib.api import API
from lib.alert import send_order_alert, send_alert

# Authentication keys
# secret_key = os.environ.get('SECRETKEY')
secret_key = "8517b4a7e07104f5605d03680859fb88ea03486608beadc093155f258904019c"
# api_key = os.environ.get('APIKEY')
api_key = "df7e0c08e87cf7d974a8acb2044ba36412b6c909a7d3a6cb073097a03a726f48"

# Create API Object
api_connector = API(secret_key, api_key)

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

def get_coin_quantity(coin_name):
    for data in user_portfolio['data']:
        if data['currency'] == coin_name:
            return float(data['main_balance'])
    return 0.0


def place_order(side, symbol, price):
    coin_name = symbol.split('/')[0]  # Convert coin name e.g. BTC/INR => BTC
    balance = get_main_balance()  # Get Fund or main balance from portfolio
    coin_exists = find_coin(coin_name)  # Check the coin exists in portfolio or not
    
    if side == 'buy':
        buy_quantity = 100 / price  # Calculate buy quantity (Note: Always invest 100 INR from portfolio balance)
        if balance >= 110:
            payload = {
                "side": side,
                "symbol": symbol,
                "type": "limit",
                "price": price,
                "quantity": buy_quantity,
                "exchange": "coinswitchx"
            }
            response = api_connector.create_order(payload=payload)
            if response.get("status") == "success":
                send_order_alert(side, symbol, price, buy_quantity, balance)
            else:
                send_alert(f"Buy Order failed: {response.get('message', 'Unknown error')}")
        else:
            send_alert("Insufficient funds for trade! Please add more than 110 INR.")
    
    elif side == 'sell' and coin_exists:
        sell_quantity = get_coin_quantity(coin_name)  # Get coin quantity from portfolio
        if sell_quantity > 0:
            payload = {
                "side": side,
                "symbol": symbol,
                "type": "limit",
                "price": price,
                "quantity": sell_quantity,
                "exchange": "coinswitchx"
            }
            response = api_connector.create_order(payload=payload)
            if response.get("status") == "success":
                send_order_alert(side, symbol, price, sell_quantity, balance)
            else:
                send_alert(f"Sell Order failed: {response.get('message', 'Unknown error')}")
