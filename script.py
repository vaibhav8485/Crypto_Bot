# STD Modules
import logging

# User Define Modules
from lib.dataset import get_data  # Get dataset
from lib.signal import get_signal  # Get signal 
from lib.order import place_order  # Place orders to coin switch exchange 

# Basic configuration for logging
logging.basicConfig(level=logging.INFO)

# Crypto Watch list
watchlist = ["BTC/INR", "ETH/INR", "MATIC/INR", "XRP/INR", "ADA/INR", "BAT/INR", "BNB/INR", "SOL/INR", "NEAR/INR", "SAND/INR", "DOGE/INR", "SHIB/INR", "STX/INR"] # It's carry [13] Crypto

# Main Function
def CRYPTO_BOT():
    try:
        logging.info("[Start]")
        for asset in watchlist:     
            
            df_1d = get_data(asset, '1d', 1000) # Get 1 Day OHLCV data
            df_1w = get_data(asset, '1w', 1000) # Get 1 Week OHLCV data
            
            # Check if the dataframes are empty
            if df_1d.empty or df_1w.empty:
                logging.warning(f"No data available for {asset}. Skipping.")
                continue
            
            result_1d, b1_1d, s1_1d, h1_1d, b2_1d, s2_1d, h2_1d = get_signal(df_1d) # Get 1 Day Signal
            result_1w, b1_1w, s1_1w, h1_1w, b2_1w, s2_1w, h2_1w = get_signal(df_1w) # Get 1 Week Signal
            
            if result_1d == 1 and result_1w == 1: # For BUY
                place_order('buy', asset, result_1d, result_1w, b1_1d, b2_1d, b1_1w, b2_1w, h1_1d, h2_1d, h1_1w, h2_1w)
                logging.info(f"Buy order placed for {asset}")
            elif result_1d == 0 and result_1w == 0: # For SELL
                place_order('sell', asset, result_1d, result_1w, s1_1d, s2_1d, s1_1w, s2_1w, h1_1d, h2_1d, h1_1w, h2_1w)
                logging.info(f"Sell order placed for {asset}")

        logging.info("[End]")
    except Exception as e:
        logging.error(f"An unexpected error occurred in Crypto Bot: {e}")

# Execution Start form this
if __name__ == "__main__":
    CRYPTO_BOT()
