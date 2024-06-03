import ccxt
import pandas as pd
import time
import logging

# Initialize CCXT Exchange
exchange = ccxt.wazirx()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Get Dataset with Retry Logic
def get_data(symbol, timeframe, limit, retries=5, delay=5):
    attempt = 0
    while attempt < retries:
        try:
            # Fetch All Data
            data = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            ticker = exchange.fetch_ticker(symbol)
            df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)

            # Return data frame
            return df
        
        except ccxt.NetworkError as e:
            logging.error(f"Network error occurred: {e}. Retrying in {delay} seconds...")
            time.sleep(delay)
            attempt += 1
        
        except ccxt.ExchangeError as e:
            logging.error(f"Exchange error occurred: {e}. Retrying in {delay} seconds...")
            time.sleep(delay)
            attempt += 1
        
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            break

    # Return an empty DataFrame in case of failure
    logging.error(f"Failed to fetch data for {symbol} after {retries} attempts.")
    return pd.DataFrame(columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
