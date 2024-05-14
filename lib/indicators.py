import ta
import numpy as np

# Momentum Indicators
class Momentum_Indicators:
    def __init__(self, df):
        self.df = df

    def rsi(self, window=14, threshold_high=70, threshold_low=30):
        try:
            # Calculate RSI with the specified window
            rsi_indicator = ta.momentum.RSIIndicator(close=self.df['close'], window=window)
            # Get RSI values
            rsi_values = rsi_indicator.rsi()
            # Add RSI values to the dataframe
            self.df['rsi'] = rsi_values
            # Initialize the 'Signal' column with 'NA'
            self.df['signal'] = 'NA'
            # Update 'Signal' column based on RSI thresholds
            self.df.loc[self.df['rsi'] >= threshold_high, 'signal'] = 0
            self.df.loc[self.df['rsi'] <= threshold_low, 'signal'] = 1

            # Set priority
            p = 5

            return self.df['signal'].iloc[-1], p
        
        except Exception as e:
            print(f"An error occurred in RSI calculation: {e}")

    def roc(self, window=9):
        try:
            # Calculate ROC with the specified window
            roc = ta.momentum.ROCIndicator(close=self.df['close'], window=window)
            # Add ROC values to the dataframe
            self.df['roc'] = roc.roc()

            # Assign signals based on ROC values
            self.df['signal'] = np.where(self.df['roc'] < 0, 1, 0)

            # Set priority
            p = 4

            return self.df['signal'].iloc[-1], p
        
        except Exception as e:
            print(f"An error occurred in ROC calculation: {e}")

    def so(self, window=14, smooth_window=1, threshold_high=80, threshold_low=20):
        try:
            # Calculate Stochastic Oscillator with the specified parameters
            stoch_indicator = ta.momentum.StochasticOscillator(high=self.df['high'], low=self.df['low'], close=self.df['close'], window=window, smooth_window=smooth_window)
            # Get %K values
            percent_k = stoch_indicator.stoch()
            # Add %K values to the dataframe
            self.df['%K'] = percent_k
            # Initialize the 'Signal' column with 'NA'
            self.df['signal'] = 'NA'
            # Update 'Signal' column based on %K thresholds
            self.df.loc[self.df['%K'] >= threshold_high, 'signal'] = 0
            self.df.loc[self.df['%K'] <= threshold_low, 'signal'] = 1
        
            # Set priority
            p = 4

            return self.df['signal'].iloc[-1], p
        
        except Exception as e:
            print(f"An error occurred in Stochastic Oscillator calculation: {e}")

    def macd(self, window_slow=26, window_fast=12, window_sign=9):
        try:
            # Calculate MACD with the specified parameters
            macd_indicator = ta.trend.MACD(close=self.df['close'], window_slow=window_slow, window_fast=window_fast, window_sign=window_sign)
            # Get MACD line, signal line, and histogram values
            macd_line = macd_indicator.macd()
            signal_line = macd_indicator.macd_signal()
            macd_histogram = macd_indicator.macd_diff()
            # Add MACD values to the dataframe
            self.df['macd_line'] = macd_line
            self.df['macd_signal'] = signal_line
            self.df['macd_histogram'] = macd_histogram
            # Initialize the 'Signal' column with 'NA'
            self.df['signal'] = 'NA'
            self.df['zero_line'] = 0
            # Update 'Signal' column based on MACD and Signal line crossover
            self.df.loc[(self.df['macd_line'] > self.df['macd_signal']), 'signal'] = 0
            self.df.loc[(self.df['macd_line'] < self.df['macd_signal']), 'signal'] = 1
            self.df.loc[(self.df['macd_line'] < 0) & (self.df['macd_signal'] < 0), 'zero_line'] = 1

            # Set priority
            p = 5

            return self.df['signal'].iloc[-1], self.df['zero_line'].iloc[-1], p
        
        except Exception as e:
            print(f"An error occurred in MACD calculation: {e}")


# Trend Indicators
class Trend_Indicators:
    def __init__(self, df):
        self.df = df

    def aroon(self, window=14):
        try:
            # Calculate Aroon indicator
            aroon_indicator = ta.trend.AroonIndicator(high=self.df['high'], low=self.df['low'], window=window)
            # Add Aroon Up and Aroon Down lines to DataFrame
            self.df['aroon_up'] = aroon_indicator.aroon_up()
            self.df['aroon_down'] = aroon_indicator.aroon_down()
            # Initialize 'Signal' column with NaN values
            self.df['signal'] = "NA"
            # Generate signals based on Aroon indicator reaching 100
            self.df.loc[self.df['aroon_up'] == 100, 'signal'] = 0
            self.df.loc[self.df['aroon_down'] == 100, 'signal'] = 1
        
            # Set priority
            p = 4

            return self.df['signal'].iloc[-1], p
        
        except Exception as e:
            print(f"An error occurred in Aroon calculation: {e}")

    def ema(self, window=14):
        try:
            self.df['ema'] = ta.trend.ema_indicator(close=self.df['close'], window=window)
            # Add buy and sell signals based on EMA and close price comparison
            self.df['signal'] = np.where(self.df['ema'] > self.df['close'], 1, 0)
            
            # Set priority
            p = 3

            return self.df['signal'].iloc[-1], p
        
        except Exception as e:
            print(f"An error occurred in EMA calculation: {e}")

    def wma(self, window=9):
        try:
            # Calculate WMA
            self.df['wma'] = ta.trend.wma_indicator(close=self.df['close'], window=window)
            # Add buy and sell signals based on WMA and close price comparison
            self.df['signal'] = np.where(self.df['wma'] > self.df['close'], 1, 0)
        
            # Set priority
            p = 3

            return self.df['signal'].iloc[-1], p
        
        except Exception as e:
            print(f"An error occurred in WMA calculation: {e}")

    def sma(self, window=14):
        try:
            # Calculate SMA
            self.df['sma'] = ta.trend.sma_indicator(close=self.df['close'], window=window)
            # Add buy and sell signals based on SMA and close price comparison
            self.df['signal'] = np.where(self.df['sma'] > self.df['close'], 1, 0)
        
            # Set priority
            p = 3

            return self.df['signal'].iloc[-1], p
        
        except Exception as e:
            print(f"An error occurred in SMA calculation: {e}")


# Volatility Indicators
class Volatility_Indicators:
    def __init__(self, df):
        self.df = df

    def bb(self):
        try:
            # Calculate Bollinger Bands
            bb = ta.volatility.BollingerBands(self.df['close'], window=20, window_dev=2)

            # Add Bollinger Bands values to the dataframe
            self.df['upper_band'] = bb.bollinger_hband()
            self.df['middle_band'] = bb.bollinger_mavg()
            self.df['lower_band'] = bb.bollinger_lband()

            # Determine volatility signal
            self.df['signal'] = 'NA'
            self.df.loc[self.df['high'] >= self.df['upper_band'], 'signal'] = 0
            self.df.loc[self.df['low'] <= self.df['lower_band'], 'signal'] = 1

            # Set priority
            p = 3

            return self.df['signal'].iloc[-1], p

        except Exception as e:
            print(f"An error occurred in Bollinger Bands calculation: {e}")

    def adx(self, window=14, threshold=25):
        try:
            # Calculate ADX
            self.df['adx'] = ta.trend.adx(self.df['high'], self.df['low'], self.df['close'], window=window)

            # Determine volatility signal
            self.df['signal'] = np.where(self.df['adx'] < threshold, 1, 0)

            # Set priority
            p = 2

            return self.df['signal'].iloc[-1], p

        except Exception as e:
            print(f"An error occurred in ADX calculation: {e}")

    def kc(self, window=20):
        try:
            # Calculate Keltner Channel
            kc = ta.volatility.KeltnerChannel(high=self.df['high'], low=self.df['low'], close=self.df['close'], window=window)
            self.df['upper_band'] = kc.keltner_channel_hband()
            self.df['middle_band'] = kc.keltner_channel_mband()
            self.df['lower_band'] = kc.keltner_channel_lband()

            # Determine volatility signal
            self.df['signal'] = 'NA'  # Default to High volatility

            self.df.loc[self.df['high'] >= self.df['upper_band'], 'signal'] = 0
            self.df.loc[self.df['low'] <= self.df['lower_band'], 'signal'] = 1

            # Set priority
            p = 2

            return self.df['signal'].iloc[-1], p

        except Exception as e:
            print(f"An error occurred in Keltner Channel calculation: {e}")

    def dc(self, window=20):
        try:
            # Calculate Donchian Channel
            dc = ta.volatility.DonchianChannel(high=self.df['high'], low=self.df['low'], close=self.df['close'], window=window)
            self.df['upper_band'] = dc.donchian_channel_hband()
            self.df['middle'] = dc.donchian_channel_mband()
            self.df['lower_band'] = dc.donchian_channel_lband()

            # Determine volatility signal
            self.df['signal'] = 'NA'
            self.df.loc[self.df['high'] >= self.df['upper_band'], 'signal'] = 0
            self.df.loc[self.df['low'] <= self.df['lower_band'], 'signal'] = 1

            # Set priority
            p = 2

            return self.df['signal'].iloc[-1], p

        except Exception as e:
            print(f"An error occurred in Donchian Channel calculation: {e}")


# Volume Indicators
class Volume_Indicators:
    def __init__(self, df):
        self.df = df

    def obv(self, threshold_low=0.03, threshold_high=0.07):
        try:
            # Calculate OBV
            obv_data = ta.volume.OnBalanceVolumeIndicator(self.df['close'], self.df['volume'])

            # Add OBV values to the DataFrame
            self.df['obv'] = obv_data.on_balance_volume()

            # Identify volume levels based on thresholds
            self.df['signal'] = 'NA'
            self.df.loc[self.df['obv'] > threshold_high, 'signal'] = 0
            self.df.loc[self.df['obv'] < threshold_low, 'signal'] = 1

            # Set priority
            p = 1

            return self.df['signal'].iloc[-1], p

        except Exception as e:
            print(f"An error occurred in OBV calculation: {e}")

    def cmf(self, window=20):
        try:
            # Calculate CMF
            cmf = ta.volume.ChaikinMoneyFlowIndicator(high=self.df['high'], low=self.df['low'], close=self.df['close'], volume=self.df['volume'], window=window)
            self.df['cmf'] = cmf.chaikin_money_flow()

            # Assign signal based on CMF value
            self.df['signal'] = 'NA'
            self.df.loc[self.df['cmf'] > 0, 'signal'] = 0
            self.df.loc[self.df['cmf'] < 0, 'signal'] = 1

            # Set priority
            p = 1

            return self.df['signal'].iloc[-1], p

        except Exception as e:
            print(f"An error occurred in CMF calculation: {e}")

    def eom(self, window=14):
        try:
            eom = ta.volume.EaseOfMovementIndicator(self.df['high'], self.df['low'], self.df['volume'], window=window)
            self.df['eom'] = eom.sma_ease_of_movement()
            self.df['signal'] = 'NA'
            self.df.loc[self.df['eom'] > 0, 'signal'] = 0
            self.df.loc[self.df['eom'] < 0, 'signal'] = 1

            # Set priority
            p = 1

            return self.df['signal'].iloc[-1], p

        except Exception as e:
            print(f"An error occurred in EOM calculation: {e}")

    def mfi(self, window=14, threshold_high=80, threshold_low=20):
        try:
            # Calculate MFI
            mfi = ta.volume.MFIIndicator(high=self.df['high'], low=self.df['low'], close=self.df['close'], volume=self.df['volume'], window=window)
            self.df['mfi'] = mfi.money_flow_index()

            # Assign signal based on MFI value
            self.df['signal'] = 'NA'
            self.df.loc[self.df['mfi'] >= threshold_high, 'signal'] = 0
            self.df.loc[self.df['mfi'] <= threshold_low, 'signal'] = 1

            # Set priority
            p = 1

            return self.df['signal'].iloc[-1], p

        except Exception as e:
            print(f"An error occurred in MFI calculation: {e}")
