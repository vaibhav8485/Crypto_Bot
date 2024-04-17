# User Define Modules
from lib.indicator import MACD, RSI, PRICE_MOMENTUM, SO # (Technical Indicator)
from lib.alert import send_alert

# Parameters for MACD Indicator
signal_input = 9
macd_short_period = 12
macd_long_period = 26

# Parameters for RSI Indicator
rsi_period = 14
below_line = 30
above_line = 60

# Parameters for Price Momentum Indicator (PPO)
period = 7

# Parameters for Stochastic Oscillator Indicator (SO)
k_period = 14
d_period = 1

# Get Signal
def get_signal(df, symbol_name, current_price):

    try:
        # MACD
        macd_signal, macd_signal_line = MACD(df, symbol_name, signal_input, macd_short_period, macd_long_period)
        
        # RSI
        rsi_signal, rsi_signal_line = RSI(df, symbol_name, rsi_period, below_line, above_line)

        # Price Percentage Oscillator (PPO)
        ppo_signal, ppo_value = PRICE_MOMENTUM(df, symbol_name, period)

        # Stochastic Oscillator (SO)
        so_signal, k_value = SO(df, k_period, d_period)

        # Final Result / Action
        buy_count = 0
        sell_count = 0
        hold_count = 0
        
        # MACD 
        if macd_signal == 'UpTrend' and macd_signal_line < 0:
            buy_count += 1
        elif macd_signal == 'DownTrend' and macd_signal_line > 0:
            sell_count += 1
        else:
            hold_count += 1

        # RSI
        if rsi_signal == 'Oversold' and rsi_signal_line <= 30:
            buy_count += 1
        elif rsi_signal == 'Overbought' and rsi_signal_line >= 60:
            sell_count += 1
        else:
            hold_count += 1    

        # PPO
        if ppo_signal == 'Oversold' and ppo_value < 0: 
            buy_count += 1
        elif ppo_signal == 'Overbought' and ppo_value > 0:
            sell_count += 1
        else:
            hold_count += 1

        # SO
        if so_signal == 'Oversold' and k_value <= 20:
            buy_count += 1
        elif so_signal == 'Overbought' and k_value >= 80: 
            sell_count += 1
        else:
            hold_count += 1

        # Action
        if buy_count > sell_count and buy_count > hold_count:
            final_result = 'Buy'
        elif sell_count > buy_count and sell_count > hold_count:
            final_result = 'Sell'
        else:
            final_result = 'Hold'

        # Send Alert
        if final_result != 'Hold':
            send_alert(str(final_result), str(symbol_name), str(current_price), str(macd_signal), str(macd_signal_line), str(rsi_signal), str(rsi_signal_line), str(ppo_signal), str(ppo_value), str(so_signal), str(k_value))


    except Exception as e:
        print(f"An unexpected error occurred in Signal Section: {e}")
    