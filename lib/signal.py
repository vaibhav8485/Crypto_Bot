# User Define Modules
from lib.indicators import Momentum_Indicators, Trend_Indicators, Volatility_Indicators, Volume_Indicators

def get_signal(df):
    try:
        # Initialize indicator classes
        momentum = Momentum_Indicators(df)
        trend = Trend_Indicators(df)
        volatility = Volatility_Indicators(df)
        volume = Volume_Indicators(df)

        # Get signals and probabilities
        rsi_signal, rsi_p = momentum.rsi()
        roc_signal, roc_p = momentum.roc()
        so_signal, so_p = momentum.so()
        macd_signal, macd_zero_line, macd_p = momentum.macd()

        aroon_signal, aroon_p = trend.aroon() 
        ema_signal, ema_p = trend.ema()
        wma_signal, wma_p = trend.wma()
        sma_signal, sma_p = trend.sma()

        bb_signal, bb_p = volatility.bb()
        adx_signal, adx_p = volatility.adx()
        kc_signal, kc_p = volatility.kc()
        dc_signal, dc_p = volatility.dc()

        obv_signal, obv_p = volume.obv()
        cmf_signal, cmf_p = volume.cmf()
        eom_signal, eom_p = volume.eom()
        mfi_signal, mfi_p = volume.mfi()

        # Initialize as 0
        buy_count = 0
        sell_count = 0
        hold_count = 0

        momentum_buy = 0
        momentum_sell = 0
        momentum_hold = 0

        trend_buy = 0
        trend_sell = 0
        trend_hold = 0

        volatility_buy = 0
        volatility_sell = 0
        volatility_hold = 0

        volume_buy = 0
        volume_sell = 0
        volume_hold = 0

        # Momentum
        momentum_buy += rsi_p if rsi_signal == 1 else 0
        momentum_sell += rsi_p if rsi_signal == 0 else 0
        momentum_hold += rsi_p if rsi_signal == 'NA' else 0
        momentum_buy += roc_p if roc_signal == 1 else 0
        momentum_sell += roc_p if roc_signal == 0 else 0
        momentum_buy += so_p if so_signal == 1 else 0
        momentum_sell += so_p if so_signal == 0 else 0
        momentum_hold += so_p if so_signal == 'NA' else 0
        momentum_buy += macd_p if macd_signal == 1 and macd_zero_line == 1 else 0
        momentum_sell += macd_p if macd_signal == 0 and macd_zero_line == 0 else 0
        momentum_buy += macd_p if macd_signal == 1 and macd_zero_line == 0 else 0
        momentum_sell += macd_p if macd_signal == 0 and macd_zero_line == 1 else 0

        # Trend
        trend_buy += aroon_p if aroon_signal == 1 else 0
        trend_sell += aroon_p if aroon_signal == 0 else 0
        trend_hold += aroon_p if aroon_signal == 'NA' else 0
        trend_buy += ema_p if ema_signal == 1 else 0
        trend_sell += ema_p if ema_signal == 0 else 0
        trend_buy += wma_p if wma_signal == 1 else 0
        trend_sell += wma_p if wma_signal == 0 else 0
        trend_buy += sma_p if sma_signal == 1 else 0
        trend_sell += sma_p if sma_signal == 0 else 0

        # Volatility
        volatility_buy += bb_p if bb_signal == 1 else 0
        volatility_sell += bb_p if bb_signal == 0 else 0
        volatility_hold += bb_p if bb_signal == 'NA' else 0
        volatility_buy += adx_p if adx_signal == 1 else 0
        volatility_sell += adx_p if adx_signal == 0 else 0
        volatility_buy += kc_p if kc_signal == 1 else 0
        volatility_sell += kc_p if kc_signal == 0 else 0
        volatility_hold += kc_p if kc_signal == 'NA' else 0
        volatility_buy += dc_p if dc_signal == 1 else 0
        volatility_sell += dc_p if dc_signal == 0 else 0
        volatility_hold += dc_p if dc_signal == 'NA' else 0

        # Volume
        volume_buy += obv_p if obv_signal == 1 else 0
        volume_sell += obv_p if obv_signal == 0 else 0
        volume_hold += obv_p if obv_signal == 'NA' else 0
        volume_buy += cmf_p if cmf_signal == 1 else 0
        volume_sell += cmf_p if cmf_signal == 0 else 0
        volume_hold += cmf_p if cmf_signal == 'NA' else 0
        volume_buy += eom_p if eom_signal == 1 else 0
        volume_sell += eom_p if eom_signal == 0 else 0
        volume_hold += eom_p if eom_signal == 'NA' else 0
        volume_buy += mfi_p if mfi_signal == 1 else 0
        volume_sell += mfi_p if mfi_signal == 0 else 0
        volume_hold += mfi_p if mfi_signal == 'NA' else 0

        # Aggregate buy, sell, and hold counts
        buy_count = momentum_buy + trend_buy + volatility_buy + volume_buy
        sell_count = momentum_sell + trend_sell + volatility_sell + volume_sell
        hold_count = momentum_hold + trend_hold + volatility_hold + volume_hold

        # Determine final signal based on the counts
        if buy_count > sell_count and buy_count > hold_count:
            final_signal = 1
        elif sell_count > buy_count and sell_count > hold_count:
            final_signal = 0
        elif hold_count > buy_count and hold_count > sell_count:
            final_signal = 'Hold'
        else:
            final_signal = 'Hold'

        # Return Final Signal
        return final_signal, momentum_buy, momentum_sell, trend_buy, trend_sell, volatility_buy, volatility_sell, volume_buy, volume_sell

    except Exception as e:
        print(f"An unexpected error occurred in Signal Section: {e}")
