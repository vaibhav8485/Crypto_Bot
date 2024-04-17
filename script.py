# STD Modules
import time # For Time Operation

# User Define Modules
from lib.dataset import get_data  # Get Dataset
from lib.signal import get_signal  # Get Signal

# Param For Dataset
watchlist = ["BTC/INR", "ETH/INR", "MATIC/INR", "XRP/INR", "ADA/INR", "BAT/INR", "BNB/INR", "SOL/INR","NEAR/INR", "SAND/INR", "DOGE/INR", "SHIB/INR", "STX/INR"]
watchlist_timeframe = '1w'
watchlist_limit = 1000

def CRYPTO_BOT():
    try:
        print("[Start]")
        # Iterate through each asset
        for asset in watchlist:
            # Get Data for current asset
            df, symbol_name, asset_price = get_data(asset, watchlist_timeframe, watchlist_limit)
            # Get Conclusion
            get_signal(df, symbol_name, asset_price)
            # Sleep for 1 second
            time.sleep(1)
        print("[End]")
    except Exception as e:
        print(f"An unexpected error occurred in Crypto Bot : {e}")

# CRYPTO_BOT()
if __name__ == "__main__":
    CRYPTO_BOT()