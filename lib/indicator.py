# IMP STD Modules
import numpy as np
import talib

def MACD(df, symbol_name, signal_input, short_macd, long_macd):

    """
    Calculate MACD signals based on crossover of short-term and long-term MACD.

    Parameters:
    - df (DataFrame): Historical price data DataFrame.
    - signal_input (int): MACD signal line window size.
    - short_macd (int): Short-term MACD window size.
    - long_macd (int): Long-term MACD window size.

    Returns:
    MACD DATA.
    """

    try:
        # Calculate Short-term and Long-term Exponential Moving Averages
        df['Short_EMA'] = df['close'].ewm(span=short_macd, adjust=False).mean()
        df['Long_EMA'] = df['close'].ewm(span=long_macd, adjust=False).mean()
    
        # Calculate MACD line
        df['MACD'] = df['Short_EMA'] - df['Long_EMA']
    
        # Calculate Signal line
        df['Signal_Line'] = df['MACD'].ewm(span=signal_input, adjust=False).mean()
    
        # Calculate Zero line
        zero_line_value = 0
    
        # Generate signals (Buy: MACD crosses above Signal Line or Zero Line, Sell: MACD crosses below Signal Line or Zero Line)
        df['signal'] = 'No Action'  # 'No Action': No signal, 'Buy': Buy signal, 'Sell': Sell signal
        df.iloc[short_macd:, df.columns.get_loc('signal')] = np.where((df['MACD'].iloc[short_macd:] > df['Signal_Line'].iloc[short_macd:]) | (df['MACD'].iloc[short_macd:] > zero_line_value), 'UpTrend', np.where((df['MACD'].iloc[short_macd:] < df['Signal_Line'].iloc[short_macd:]) | (df['MACD'].iloc[short_macd:] < zero_line_value), 'DownTrend', 'Neutral'))
    
       # Download Dataset in CSV formate
        # file_name = f'....PATH....{symbol_name}.csv'
        # df.to_csv(file_name) 

        signal = df['signal'].iloc[-1] # MACD Signal
        signal_line = df['Signal_Line'].iloc[-1] # Signal Line    

        # Return MACD Data
        return signal, signal_line
    
    except Exception as e:
        print(f"An unexpected error occurred in MACD Indicator : {e}")


# RSI Indicator
def RSI(df, symbol_name, rsi_period, below_line, above_line):

    """
    Calculate RSI and generate buy/sell signals based on specified thresholds.

    Parameters:
    - df (DataFrame): Input DataFrame containing historical prices.
    - close_column (str): Column name for closing prices.
    - rsi_period (int): RSI calculation period.
    - below_line (float): Threshold for RSI to generate a buy signal.
    - above_line (float): Threshold for RSI to generate a sell signal.

    Returns:
    RSI DATA.
    """
    
    try:
        # Calculate RSI
        df['rsi'] = talib.RSI(df['close'], timeperiod = rsi_period)

        # Create a signal column based on RSI conditions
        df['signal'] = 'Neutral'  # Default value for "No Action"

        # Buy signal: RSI crosses below 'below_line'
        df.loc[df['rsi'] <= below_line, 'signal'] = 'Oversold'

        # Sell signal: RSI crosses above 'above_line'
        df.loc[df['rsi'] >= above_line, 'signal'] = 'Overbought' 

        # Download Dataset in CSV formate
        # file_name = f'....PATH....{symbol_name}.csv'
        # df.to_csv(file_name) 


        signal = df['signal'].iloc[-1] # RSI Signal
        signal_line = df['rsi'].iloc[-1] # RSI Signal Line


        # Return RSI Data
        return signal, signal_line

    except Exception as e:
        print(f"An unexpected error occurred in RSI Indicator : {e}")

    
def PRICE_MOMENTUM(df, symbol, short_period=10, long_period=21):
    """
    Function to calculate Percentage Price Oscillator (PPO) 10-21 indicator
    and generate buy, sell, or hold signals.

    Parameters:
    - df: DataFrame containing 'Close' prices.
    - symbol: Symbol or name of the security (not used in this function).
    - short_period: Number of periods for the short-term EMA (default: 10).
    - long_period: Number of periods for the long-term EMA (default: 21).

    Returns:
    - Signal: 'Buy', 'Sell', or 'Hold' based on the PPO value and zero line.
    """
    try:
        # Calculate short-term EMA
        short_ema = df['close'].ewm(span=short_period, adjust=False).mean()

        # Calculate long-term EMA
        long_ema = df['close'].ewm(span=long_period, adjust=False).mean()

        # Calculate PPO
        ppo = ((short_ema - long_ema) / long_ema) * 100

        # Add the PPO values to the DataFrame
        df['PPO'] = ppo

        # Determine the signal based on the PPO value and zero line
        ppo_value = df['PPO'].iloc[-1]
        zero_line = 0

        if ppo_value > zero_line:
            signal = 'Overbought'
        elif ppo_value < zero_line:
            signal = 'Oversold'
        else:
            signal = 'Neutral'

        # Return the signal and PPO value
        return signal, ppo_value
    
    except Exception as e:
        print(f"An unexpected error occurred in PPO Indicator: {e}")


def SO(df, k_period, d_period):
    """
    Calculate Stochastic Oscillator signal based on %K and %D lines.

    Parameters:
    - df (DataFrame): Historical price data DataFrame.
    - k_period (int): Period for %K calculation.
    - d_period (int): Period for %D calculation.

    Returns:
    Stochastic Oscillator signal and its numerical value.
    """

    try:
        # Calculate High and Low rolling minimum and maximum values over k_period
        df['rolling_min_low'] = df['low'].rolling(window=k_period).min()
        df['rolling_max_high'] = df['high'].rolling(window=k_period).max()

        # Calculate %K line
        df['%K'] = ((df['close'] - df['rolling_min_low']) / (df['rolling_max_high'] - df['rolling_min_low'])) * 100

        # Calculate %D line
        df['%D'] = df['%K'].rolling(window=d_period).mean()

        # Generate signals based on %K value
        df['signal'] = 'Neutral'  # Default signal
        df.loc[df['%K'] >= 80, 'signal'] = 'Overbought'  # Set signal to 'Overbought' if %K is greater than or equal to 80
        df.loc[df['%K'] <= 20, 'signal'] = 'Oversold'  # Set signal to 'Oversold' if %K is less than or equal to 20

        # Extract latest signal and its value
        signal = df['signal'].iloc[-1]  # Latest signal
        k_line = df['%K'].iloc[-1]  # Latest %K value

        # Return Stochastic Oscillator Signal and its numerical value
        return signal, k_line

    except Exception as e:
        print(f"An unexpected error occurred in Stochastic Oscillator : {e}")
