# STD Modules
import logging

# User Define Modules
from lib.dataset import get_data, get_month_data  # Get dataset
from lib.signal import get_signal  # Get signal 
from lib.order import place_order  # Place orders to coin switch exchange 

# Basic configuration for logging
logging.basicConfig(level=logging.INFO)

# Crypto Watch list
watchlist = ["BTC/INR", "ETH/INR", "MATIC/INR", "XRP/INR", "ADA/INR", "BAT/INR", "BNB/INR", "SOL/INR", "NEAR/INR", "SAND/INR", "DOGE/INR", "SHIB/INR", "STX/INR"] # It's carry [13] Crypto Assets

# Main Function
def CRYPTO_BOT():
    try:
        logging.info("[Start:Script]")
        for asset in watchlist:     
            
            df_1d = get_data(asset, '1d', 1000) # Get 1 Day OHLCV data
            df_1w = get_data(asset, '1w', 1000) # Get 1 Week OHLCV data
            df_1m = get_month_data(df_1w) # Get 1 Month OHLCV data
            
            # Check if the dataframes are empty
            if df_1d.empty or df_1w.empty:
                logging.warning(f"No data available for {asset}. Skipping.")
                continue

            result_1d, d_momentum_buy, d_momentum_sell, d_trend_buy, d_trend_sell, d_volatility_buy, d_volatility_sell, d_volume_buy, d_volume_sell = get_signal(df_1d) # Get 1 Day Signal
            result_1w, w_momentum_buy, w_momentum_sell, w_trend_buy, w_trend_sell, w_volatility_buy, w_volatility_sell, w_volume_buy, w_volume_sell = get_signal(df_1w) # Get 1 Week Signal
            result_1m, m_momentum_buy, m_momentum_sell, m_trend_buy, m_trend_sell, m_volatility_buy, m_volatility_sell, m_volume_buy, m_volume_sell  = get_signal(df_1m) # Get 1 Month Signal
            
            if result_1d == 1 and result_1w == 1: # For BUY
                place_order('buy', asset, result_1d, result_1w, result_1m, d_momentum_buy, d_trend_buy, d_volatility_buy, d_volume_buy, d_momentum_sell, d_trend_sell, d_volatility_sell, d_volume_sell, w_momentum_buy, w_momentum_sell, w_trend_buy, w_trend_sell, w_volatility_buy, w_volatility_sell, w_volume_buy, w_volume_sell, m_momentum_buy, m_momentum_sell, m_trend_buy, m_trend_sell, m_volatility_buy, m_volatility_sell, m_volume_buy, m_volume_sell)
                logging.info(f"Buy order placed for {asset}")
            
            elif result_1d == 0 and result_1w == 0: # For SELL
                place_order('sell', asset, result_1d, result_1w, result_1m, d_momentum_buy, d_trend_buy, d_volatility_buy, d_volume_buy, d_momentum_sell, d_trend_sell, d_volatility_sell, d_volume_sell, w_momentum_buy, w_momentum_sell, w_trend_buy, w_trend_sell, w_volatility_buy, w_volatility_sell, w_volume_buy, w_volume_sell, m_momentum_buy, m_momentum_sell, m_trend_buy, m_trend_sell, m_volatility_buy, m_volatility_sell, m_volume_buy, m_volume_sell)
                logging.info(f"Sell order placed for {asset}")

        logging.info("[End:Script]")
    except Exception as e:
        logging.error(f"An unexpected error occurred in Crypto Bot: {e}")

# Execution Start form this
if __name__ == "__main__":
    CRYPTO_BOT() # Calling Main Function
