# User Define Modules
from lib.dataset import get_data  # Get dataset
from lib.signal import get_signal  # Get signal 
from lib.alert import send_alert # Send Alert to Mail

watchlist = ["BTC/INR", "ETH/INR", "MATIC/INR", "XRP/INR", "ADA/INR", "BAT/INR", "BNB/INR", "SOL/INR","NEAR/INR", "SAND/INR", "DOGE/INR", "SHIB/INR", "STX/INR"]

def CRYPTO_BOT():
    try:
        print("[Start]")

        # Iterate through each asset
        for asset in watchlist:   
            
            # Get Daily (data frame)
            df_1d, coin, price = get_data(asset, '1d', 1000)
            df_1w, _, _ = get_data(asset, '1w', 1000)

            # Get Conclusion
            result_1d, b1_1d, s1_1d, h1_1d, b2_1d, s2_1d, h2_1d = get_signal(df_1d)
            result_1w, b1_1w, s1_1w, h1_1w, b2_1w, s2_1w, h2_1w = get_signal(df_1w)

            # Cal Final Result
            if result_1d == 1 and result_1w == 1:
                send_alert('Buy', coin, price, result_1d, result_1w, b1_1d, b2_1d, b1_1w, b2_1w, h1_1d, h2_1d, h1_1w, h2_1w)
            elif result_1d == 0 and result_1w == 0:
                send_alert('Sell', coin, price, result_1d, result_1w, s1_1d, s2_1d, s1_1w, s2_1w, h1_1d, h2_1d, h1_1w, h2_1w)

        print("[End]")
    except Exception as e:
        print(f"An unexpected error occurred in Crypto Bot : {e}")

# CRYPTO_BOT()
if __name__ == "__main__":
    CRYPTO_BOT()
