# User Define Modules
from lib.api import get_main_balance, get_coin_quantity, buy_order, sell_order
from lib.alert import send_alert, send_order_alert

# Main Function
def place_order(side, symbol):
    balance = get_main_balance() # Get fund or main balance from portfolio
    if side == 'buy': 
        if balance >= 200: # Check Fund is Enough or Not
            result = buy_order(symbol)
            send_order_alert(side, result)
        else:
            send_alert('Insufficient funds for trade [Mini: 210 INR]')
    elif side == 'sell':
        sell_quantity = get_coin_quantity(symbol)  # Get coin quantity from portfolio      
        if sell_quantity > 0: # Check Quantity is Enough for Sell
            result = sell_order(symbol)
            send_order_alert(side, result)
            