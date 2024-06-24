# STD Modules
import ta
import numpy as np
import pandas as pd


# Momentum Indicators
class Momentum_Indicators:
    def __init__(self, df):
        if not isinstance(df, pd.DataFrame):
            raise ValueError("The input df must be a pandas DataFrame")
        required_columns = ['open','close', 'high', 'low', 'volume']
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"The DataFrame must contain the columns [Momentum Indicators]: {', '.join(required_columns)}")
        self.original_df = df.copy()

    def rsi(self, window=14, threshold_high=70, threshold_low=30):
        try:
            # Make a copy of the original DataFrame
            self.df = self.original_df.copy()
            
            # Validate input parameters
            if not isinstance(window, int) or window <= 0:
                raise ValueError("Window size must be a positive integer")
            if not (0 <= threshold_low < threshold_high <= 100):
                raise ValueError("Thresholds must be in the range [0, 100] and threshold_low < threshold_high")

            # Calculate RSI with the specified window
            rsi_indicator = ta.momentum.RSIIndicator(close=self.df['close'], window=window)
            # Get RSI values
            rsi_values = rsi_indicator.rsi()
            # Add RSI values to the dataframe, handling NaN values
            self.df['rsi'] = rsi_values.fillna(0)  # Filling NaN with 0 for the sake of example; adjust as needed
            # Initialize the 'Signal' column with 'NA'
            self.df['signal'] = 'NA'
            # Update 'Signal' column based on RSI thresholds
            self.df.loc[self.df['rsi'] >= threshold_high, 'signal'] = 0
            self.df.loc[self.df['rsi'] <= threshold_low, 'signal'] = 1
            # Optionally, handle the 'middle' signals (neither overbought nor oversold)
            self.df.loc[(self.df['rsi'] > threshold_low) & (self.df['rsi'] < threshold_high), 'signal'] = 'NA'

            return self.df['signal'].iloc[-1], 3 
        
        except Exception as e:
            print(f"An error occurred in RSI calculation: {e}")

    def roc(self, window=9):
        try:
            # Make a copy of the original DataFrame
            self.df = self.original_df.copy()

            # Validate input parameters
            if not isinstance(window, int) or window <= 0:
                raise ValueError("Window size must be a positive integer")

            # Calculate ROC with the specified window
            roc = ta.momentum.ROCIndicator(close=self.df['close'], window=window)
            # Get ROC values
            self.df['roc'] = roc.roc().fillna(0)
            # Assign signals based on ROC values
            self.df['signal'] = np.where(self.df['roc'] < 0, 1, 0)

            return self.df['signal'].iloc[-1], 2
        
        except Exception as e:
            print(f"An error occurred in ROC calculation: {e}")

    def so(self, window=14, smooth_window=1, threshold_high=80, threshold_low=20):
        try:
            # Make a copy of the original DataFrame
            self.df = self.original_df.copy()

            # Validate input parameters
            if not isinstance(window, int) or window <= 0:
                raise ValueError("Window size must be a positive integer")
            if not isinstance(smooth_window, int) or smooth_window <= 0:
                raise ValueError("Smooth window size must be a positive integer")
            if not (0 <= threshold_low < threshold_high <= 100):
                raise ValueError("Thresholds must be in the range [0, 100] and threshold_low < threshold_high")
            if not all(col in self.df.columns for col in ['high', 'low', 'close']):
                raise ValueError("The DataFrame must contain the columns: 'high', 'low', 'close'")

            # Calculate Stochastic Oscillator with the specified parameters
            stoch_indicator = ta.momentum.StochasticOscillator(
                high=self.df['high'], low=self.df['low'], close=self.df['close'], window=window, smooth_window=smooth_window
            )
            # Get %K values
            percent_k = stoch_indicator.stoch()
            # Add %K values to the dataframe
            self.df['%K'] = percent_k.fillna(0)
            # Initialize the 'Signal' column with 'NA'
            self.df['signal'] = 'NA'
            # Update 'Signal' column based on %K thresholds
            self.df.loc[self.df['%K'] >= threshold_high, 'signal'] = 0
            self.df.loc[self.df['%K'] <= threshold_low, 'signal'] = 1
            # Optionally, handle the 'middle' signals
            self.df.loc[(self.df['%K'] > threshold_low) & (self.df['%K'] < threshold_high), 'signal'] = 'NA'

            return self.df['signal'].iloc[-1], 3
        
        except Exception as e:
            print(f"An error occurred in Stochastic Oscillator calculation: {e}")

    def macd(self, window_slow=26, window_fast=12, window_sign=9):
        try:
            # Make a copy of the original DataFrame
            self.df = self.original_df.copy()

            # Validate input parameters
            if not all(isinstance(x, int) and x > 0 for x in [window_slow, window_fast, window_sign]):
                raise ValueError("All window sizes must be positive integers")
            
            # Calculate MACD with the specified parameters
            macd_indicator = ta.trend.MACD(
                close=self.df['close'], window_slow=window_slow, window_fast=window_fast, window_sign=window_sign
            )
            # Get MACD line, signal line, and histogram values
            macd_line = macd_indicator.macd()
            signal_line = macd_indicator.macd_signal()
            macd_histogram = macd_indicator.macd_diff()
            # Add MACD values to the dataframe
            self.df['macd_line'] = macd_line.fillna(0)
            self.df['macd_signal'] = signal_line.fillna(0)
            self.df['macd_histogram'] = macd_histogram.fillna(0)
            # Initialize the 'Signal' column with 'NA'
            self.df['signal'] = 'NA'
            self.df['zero_line'] = 0
            # Update 'Signal' column based on MACD and Signal line crossover
            self.df.loc[(self.df['macd_line'] > self.df['macd_signal']), 'signal'] = 0
            self.df.loc[(self.df['macd_line'] < self.df['macd_signal']), 'signal'] = 1
            self.df.loc[(self.df['macd_line'] < 0) & (self.df['macd_signal'] < 0), 'zero_line'] = 1

            return self.df['signal'].iloc[-1], self.df['zero_line'].iloc[-1], 3
        
        except Exception as e:
            print(f"An error occurred in MACD calculation: {e}")

# Trend Indicators
class Trend_Indicators:
    def __init__(self, df):
        if not isinstance(df, pd.DataFrame):
            raise ValueError("The input df must be a pandas DataFrame")
        required_columns = ['open','close', 'high', 'low', 'volume']
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"The DataFrame must contain the columns [Trend Indicators]: {', '.join(required_columns)}")
        self.original_df = df.copy()

    def aroon(self, window=14):
        try:
            # Make a copy of the original DataFrame
            self.df = self.original_df.copy()

            # Validate input parameters
            if not isinstance(window, int) or window <= 0:
                raise ValueError("Window size must be a positive integer")

            # Calculate Aroon indicator
            aroon_indicator = ta.trend.AroonIndicator(high=self.df['high'], low=self.df['low'], window=window)
            # Add Aroon Up and Aroon Down lines to DataFrame
            self.df['aroon_up'] = aroon_indicator.aroon_up().fillna(0)
            self.df['aroon_down'] = aroon_indicator.aroon_down().fillna(0)
            # Initialize 'Signal' column with NaN values
            self.df['signal'] = "NA"
            # Generate signals based on Aroon indicator reaching 100
            self.df.loc[self.df['aroon_up'] == 100, 'signal'] = 0
            self.df.loc[self.df['aroon_down'] == 100, 'signal'] = 1

            return self.df['signal'].iloc[-1], 3
        
        except Exception as e:
            print(f"An error occurred in Aroon calculation: {e}")

    def ema(self, window=9):
        try:
            # Make a copy of the original DataFrame
            self.df = self.original_df.copy()

            # Validate input parameters
            if not isinstance(window, int) or window <= 0:
                raise ValueError("Window size must be a positive integer")

            ema = ta.trend.EMAIndicator(close=self.df['close'], window=window)
            self.df['ema'] = ema.ema_indicator().fillna(0)
            # Add buy and sell signals based on EMA and close price comparison
            self.df['signal'] = np.where(self.df['close'] > self.df['ema'], 0, 1)

            return self.df['signal'].iloc[-1], 1
        
        except Exception as e:
            print(f"An error occurred in EMA calculation: {e}")

    def wma(self, window=9):
        try:
            # Make a copy of the original DataFrame
            self.df = self.original_df.copy()

            # Validate input parameters
            if not isinstance(window, int) or window <= 0:
                raise ValueError("Window size must be a positive integer")

            # Calculate WMA
            wma = ta.trend.WMAIndicator(close=self.df['close'], window=window)
            self.df['wma'] = wma.wma().fillna(0)
            # Add buy and sell signals based on WMA and close price comparison
            self.df['signal'] = np.where(self.df['close'] > self.df['wma'], 0, 1)

            return self.df['signal'].iloc[-1], 1
        
        except Exception as e:
            print(f"An error occurred in WMA calculation: {e}")

    def sma(self, window=9):
        try:
            # Make a copy of the original DataFrame
            self.df = self.original_df.copy()

            # Validate input parameters
            if not isinstance(window, int) or window <= 0:
                raise ValueError("Window size must be a positive integer")

            # Calculate SMA
            sma = ta.trend.SMAIndicator(close=self.df['close'], window=window)
            self.df['sma'] = sma.sma_indicator().fillna(0)
            # Add buy and sell signals based on SMA and close price comparison
            self.df['signal'] = np.where(self.df['close'] >= self.df['sma'], 0, 1)

            return self.df['signal'].iloc[-1], 1
        
        except Exception as e:
            print(f"An error occurred in SMA calculation: {e}")

# Volatility Indicators
class Volatility_Indicators:
    def __init__(self, df):
        if not isinstance(df, pd.DataFrame):
            raise ValueError("The input df must be a pandas DataFrame")
        required_columns = ['open', 'close', 'high', 'low', 'volume']
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"The DataFrame must contain the columns [Volatility Indicators]: {', '.join(required_columns)}")
        self.original_df = df.copy()

    def bb(self, window1=20, window2=2):
        try:
            # Make a copy of the original DataFrame
            self.df = self.original_df.copy()

            # Validate input parameters
            if not all(isinstance(x, int) and x > 0 for x in [window1, window2]):
                raise ValueError("Window sizes must be positive integers")

            # Calculate Bollinger Bands
            bb = ta.volatility.BollingerBands(self.df['close'], window=window1, window_dev=window2)
            # Add Bollinger Bands values to the dataframe, filling NaN with 0
            self.df['upper_band'] = bb.bollinger_hband().fillna(0)
            self.df['middle_band'] = bb.bollinger_mavg().fillna(0)
            self.df['lower_band'] = bb.bollinger_lband().fillna(0)
            # Determine volatility signal
            self.df['signal'] = 'NA'
            self.df.loc[self.df['high'] >= self.df['upper_band'], 'signal'] = 0
            self.df.loc[self.df['low'] <= self.df['lower_band'], 'signal'] = 1

            return self.df['signal'].iloc[-1], 3

        except Exception as e:
            print(f"An error occurred in Bollinger Bands calculation: {e}")

    def adx(self, window=14, threshold=25):
        try:
            # Make a copy of the original DataFrame
            self.df = self.original_df.copy()

            # Validate input parameters
            if not all(isinstance(x, int) and x > 0 for x in [window]):
                raise ValueError("Window size must be a positive integer")

            # Calculate ADX
            self.df['adx'] = ta.trend.adx(self.df['high'], self.df['low'], self.df['close'], window=window)
            # Determine volatility signal
            self.df['signal'] = np.where(self.df['adx'] < threshold, 1, 0)

            return self.df['signal'].iloc[-1], 2

        except Exception as e:
            print(f"An error occurred in ADX calculation: {e}")

    def kc(self, window1=20, window2=1):
        try:
            # Make a copy of the original DataFrame
            self.df = self.original_df.copy()

            # Validate input parameters
            if not all(isinstance(x, int) and x > 0 for x in [window1]):
                raise ValueError("Window size must be a positive integer")

            # Calculate Keltner Channel
            kc = ta.volatility.KeltnerChannel(high=self.df['high'], low=self.df['low'], close=self.df['close'], window=window1, window_atr=window2)
            # Add Keltner Channel values to the dataframe, filling NaN with 0
            self.df['upper_band'] = kc.keltner_channel_hband().fillna(0)
            self.df['middle_band'] = kc.keltner_channel_mband().fillna(0)
            self.df['lower_band'] = kc.keltner_channel_lband().fillna(0)
            # Determine volatility signal
            self.df['signal'] = 'NA'  # Default to High volatility
            self.df.loc[self.df['close'] >= self.df['upper_band'], 'signal'] = 0
            self.df.loc[self.df['close'] <= self.df['lower_band'], 'signal'] = 1

            return self.df['signal'].iloc[-1], 1

        except Exception as e:
            print(f"An error occurred in Keltner Channel calculation: {e}")

    def dc(self, window=20):
        try:
            # Make a copy of the original DataFrame
            self.df = self.original_df.copy()

            # Validate input parameters
            if not all(isinstance(x, int) and x > 0 for x in [window]):
                raise ValueError("Window size must be a positive integer")

            # Calculate Donchian Channel
            dc = ta.volatility.DonchianChannel(high=self.df['high'], low=self.df['low'], close=self.df['close'], window=window)
            # Add Donchian Channel values to the dataframe, filling NaN with 0
            self.df['upper_band'] = dc.donchian_channel_hband().fillna(0)
            self.df['middle_band'] = dc.donchian_channel_mband().fillna(0)
            self.df['lower_band'] = dc.donchian_channel_lband().fillna(0)
            # Determine volatility signal
            self.df['signal'] = 'NA'
            self.df.loc[self.df['high'] >= self.df['upper_band'], 'signal'] = 0
            self.df.loc[self.df['low'] <= self.df['lower_band'], 'signal'] = 1

            return self.df['signal'].iloc[-1], 2

        except Exception as e:
            print(f"An error occurred in Donchian Channel calculation: {e}")

# Volume Indicators
class Volume_Indicators:
    def __init__(self, df):
        if not isinstance(df, pd.DataFrame):
            raise ValueError("The input df must be a pandas DataFrame")
        required_columns = ['open','close', 'high', 'low', 'volume']
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"The DataFrame must contain the columns [Volume Indicators]: {', '.join(required_columns)}")
        self.original_df = df.copy()

    def obv(self, threshold_low=0.03, threshold_high=0.07):
        try:
            # Make a copy of the original DataFrame
            self.df = self.original_df.copy()

            # Validate input parameters
            if not all(isinstance(x, (int, float)) for x in [threshold_low, threshold_high]):
                raise ValueError("Thresholds must be integers or floats")

            # Calculate OBV
            obv_data = ta.volume.OnBalanceVolumeIndicator(self.df['close'], self.df['volume'])
            # Add OBV values to the DataFrame
            self.df['obv'] = obv_data.on_balance_volume()
            # Identify volume levels based on thresholds
            self.df['signal'] = 'NA'
            self.df.loc[self.df['obv'] > threshold_high, 'signal'] = 0
            self.df.loc[self.df['obv'] < threshold_low, 'signal'] = 1

            return self.df['signal'].iloc[-1], 1

        except Exception as e:
            print(f"An error occurred in OBV calculation: {e}")

    def cmf(self, window=20):
        try:
            # Make a copy of the original DataFrame
            self.df = self.original_df.copy()

            # Validate input parameters
            if not isinstance(window, int) or window <= 0:
                raise ValueError("Window size must be a positive integer")

            # Calculate CMF
            cmf = ta.volume.ChaikinMoneyFlowIndicator(high=self.df['high'], low=self.df['low'], close=self.df['close'], volume=self.df['volume'], window=window)
            self.df['cmf'] = cmf.chaikin_money_flow()
            # Assign signal based on CMF value
            self.df['signal'] = 'NA'
            self.df.loc[self.df['cmf'] > 0, 'signal'] = 0
            self.df.loc[self.df['cmf'] < 0, 'signal'] = 1

            return self.df['signal'].iloc[-1], 2

        except Exception as e:
            print(f"An error occurred in CMF calculation: {e}")

    def eom(self, window=14):
        try:
            # Make a copy of the original DataFrame
            self.df = self.original_df.copy()

            # Validate input parameters
            if not isinstance(window, int) or window <= 0:
                raise ValueError("Window size must be a positive integer")

            eom = ta.volume.EaseOfMovementIndicator(high=self.df['high'], low=self.df['low'], volume=self.df['volume'], window=window)
            self.df['eom'] = eom.ease_of_movement().fillna(0)
            self.df['signal'] = 'NA'
            self.df.loc[self.df['eom'] > 0, 'signal'] = 0
            self.df.loc[self.df['eom'] < 0, 'signal'] = 1

            return self.df['signal'].iloc[-1], 1

        except Exception as e:
            print(f"An error occurred in EOM calculation: {e}")

    def mfi(self, window=14, threshold_high=70, threshold_low=30):
        try:
            # Make a copy of the original DataFrame
            self.df = self.original_df.copy()

            # Validate input parameters
            if not all(isinstance(x, int) and x > 0 for x in [window, threshold_high, threshold_low]):
                raise ValueError("Window size and thresholds must be positive integers")

            # Calculate MFI
            mfi = ta.volume.MFIIndicator(high=self.df['high'], low=self.df['low'], close=self.df['close'], volume=self.df['volume'], window=window)
            self.df['mfi'] = mfi.money_flow_index()
            # Assign signal based on MFI value
            self.df['signal'] = 'NA'
            self.df.loc[self.df['mfi'] >= threshold_high, 'signal'] = 0
            self.df.loc[self.df['mfi'] <= threshold_low, 'signal'] = 1

            return self.df['signal'].iloc[-1], 2

        except Exception as e:
            print(f"An error occurred in MFI calculation: {e}")
