# STD Modules
import  ccxt
import pandas as pd

# Initialize CCXT Exchange
exchange = ccxt.wazirx()

# Get Dataset
def get_data(symbol, timeframe, limit):
    try:
        # Fetch All Data
        data = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        
        ticker = exchange.fetch_ticker(symbol)
        price = ticker['last']
        
        df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)

        # Get Coin Name
        coin = symbol.split('/')[0]

        # Return
        return df, coin, price
    
    except Exception as e:
        print(f"An unexpected error occurred in Day Dataset Section: {e}")
