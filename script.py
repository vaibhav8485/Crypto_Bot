# STD Modules
import logging
import os

# User Define Modules
from lib.dataset import get_data, get_month_data  # Get dataset
from lib.signal import get_signal  # Get signal 
from lib.order import place_order  # Place orders to coin switch exchange
from lib.risk import load_log_file, update_log_file, get_stop_loss, auto_status_change, get_status, get_target # Get Risk Management Functions 
from lib.api import ticker, find_coin, sell_order # Get Current Price
from lib.alert import send_alert # Send Alert Msg for Stop Loss Hit and Target Hit

# Basic configuration for logging
logging.basicConfig(level=logging.INFO)

file_path = 'log.json' # Log File Name
log_data = load_log_file(file_path) # Load Log File

# Crypto Watch list (12 Assets)
watchlist = ["BTC/INR", "ETH/INR", "MATIC/INR", "XRP/INR", "ADA/INR", "BAT/INR", "BNB/INR", "SOL/INR", "NEAR/INR", "SAND/INR", "DOGE/INR", "STX/INR"]

# Main Crypto Bot Function
def CRYPTO_BOT():
    try:
        logging.info("[Start: CRYPTO_BOT()]")
        for symbol in watchlist:
            crypto_exists = find_coin(symbol)  # Check the coin exists in portfolio or not
            current_price = ticker(symbol) # Get Current Price of Crypto
            # Auto Set Log Status
            auto_status_change(file_path, log_data, crypto_exists, symbol, current_price)
            # Get Log Status
            log_status = get_status(log_data, symbol)
                
            df_1d = get_data(symbol, '1d', 1000) # Get 1 Day OHLCV data
            df_1w = get_data(symbol, '1w', 1000) # Get 1 Week OHLCV data
            df_1m = get_month_data(df_1w) # Get 1 Month OHLCV data
            
            # Check if the dataframes are empty
            if df_1d.empty or df_1w.empty:
                logging.warning(f"No data available for {symbol}. Skipping.")
                continue

            result_1d = get_signal(df_1d) # Get 1 Day Signal
            result_1w = get_signal(df_1w) # Get 1 Week Signal
            result_1m = get_signal(df_1m) # Get 1 Month Signal

            if result_1d == 1 and result_1w == 1 and result_1m != 0 and log_status == 'auto'and crypto_exists == False: # For BUY
                place_order('buy', symbol) # Place Buy Order
                logging.info(f" Buy order placed for {symbol}") # Console Msg
            elif result_1d == 0 and result_1w == 0 and result_1m != 1 and log_status == 'auto' and crypto_exists == True: # For SELL
                place_order('sell', symbol) # Place Sell Order
                logging.info(f" Sell order placed for {symbol}") # Console Msg
        logging.info("[End: CRYPTO_BOT()]")
    except Exception as e:
        logging.error(f"An unexpected error occurred in Crypto Bot: {e}")

# Main Risk Management Function
def RISK_MANAGEMENT():
    try:
        logging.info("[Start: RISK_MANAGEMENT()]")
        for data in log_data.get('data', []):
            
            symbol = data['symbol'] # Get Crypto Name
            current_price = ticker(symbol) # Get Current Price of Crypto
            buy_price = data['buy_price'] # Get Purchasing Price of Crypto
            crypto_exists = find_coin(symbol)  # Check the coin exists in portfolio or not
            stop_loss_price = get_stop_loss(buy_price, 5) # Calculate Stop Loss Price (Note: 10%)
            target_price = get_target(buy_price, 20) # Calculate Target Price (Note: 20%)

            # For Stop Loss Hit
            if current_price <= stop_loss_price and crypto_exists == True:
                sell_order(symbol) # Place Sell Order
                update_log_file(file_path, symbol, 0, 'manual') # Update Log Status
                send_alert(f'Stop Loss Hit! Buy Back Manually Activated for {symbol}') # Send Alert
                logging.info(f"Stop Loss Hit for {symbol}") # Console Msg
            # For Target Hit
            elif current_price >= target_price and crypto_exists == True:
                update_log_file(file_path, symbol, buy_price, 'hold') # Update Log Status
                send_alert(f'Target Hit! Sell Manually Activated for {symbol}') # Send Alert
                logging.info(f'Target Hit for {symbol}') # Console Msg
        logging.info("[End: RISK_MANAGEMENT()]")
    except Exception as e:
        logging.error(f"An unexpected error occurred in Risk Management: {e}")

# Execution Start form this
if __name__ == "__main__":
    RISK_MANAGEMENT() # Calling Risk Management Function 
    CRYPTO_BOT() # Calling Main Function
