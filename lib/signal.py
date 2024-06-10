# User Define Modules
from lib.indicators import Momentum_Indicators, Trend_Indicators, Volatility_Indicators, Volume_Indicators

# Main Function
def get_signal(df):
    try:
        # Initialize indicator classes
        momentum = Momentum_Indicators(df)
        trend = Trend_Indicators(df)
        volatility = Volatility_Indicators(df)
        volume = Volume_Indicators(df)
        
        # Initialize counts
        buy_count = 0
        sell_count = 0
        hold_count = 0
        imp_buy_count = 0
        imp_sell_count = 0
        imp_hold_count = 0

        # Get signals and probabilities
        # Momentum
        rsi_signal, rsi_p = momentum.rsi()
        roc_signal, roc_p = momentum.roc()
        so_signal, so_p = momentum.so()
        macd_signal, macd_zero_line, macd_p = momentum.macd()
        # Trend
        aroon_signal, aroon_p = trend.aroon() 
        ema_signal, ema_p = trend.ema()
        wma_signal, wma_p = trend.wma()
        sma_signal, sma_p = trend.sma()
        # Volatility
        bb_signal, bb_p = volatility.bb()
        adx_signal, adx_p = volatility.adx()
        kc_signal, kc_p = volatility.kc()
        dc_signal, dc_p = volatility.dc()
        # Volume
        obv_signal, obv_p = volume.obv()
        cmf_signal, cmf_p = volume.cmf()
        eom_signal, eom_p = volume.eom()
        mfi_signal, mfi_p = volume.mfi()

        # Aggregate counts
        # Momentum
        buy_count += rsi_p if rsi_signal == 1 else 0
        sell_count += rsi_p if rsi_signal == 0 else 0
        hold_count += rsi_p if rsi_signal == 'NA' else 0

        # Imp Indicators
        imp_buy_count += rsi_p if rsi_signal == 1 else 0
        imp_sell_count += rsi_p if rsi_signal == 0 else 0
        imp_hold_count += rsi_p if rsi_signal == 'NA' else 0

        buy_count += roc_p if roc_signal == 1 else 0
        sell_count += roc_p if roc_signal == 0 else 0

        buy_count += so_p if so_signal == 1 else 0
        sell_count += so_p if so_signal == 0 else 0
        hold_count += so_p if so_signal == 'NA' else 0

        # Imp Indicators
        imp_buy_count += so_p if so_signal == 1 else 0
        imp_sell_count += so_p if so_signal == 0 else 0
        imp_hold_count += so_p if so_signal == 'NA' else 0

        buy_count += macd_p if macd_signal == 1 and macd_zero_line == 1 else 0
        sell_count += macd_p if macd_signal == 0 and macd_zero_line == 0 else 0
        buy_count += macd_p if macd_signal == 1 and macd_zero_line == 0 else 0
        sell_count += macd_p if macd_signal == 0 and macd_zero_line == 1 else 0

        # Imp Indicators
        imp_buy_count += macd_p if macd_signal == 1 and macd_zero_line == 1 else 0
        imp_sell_count += macd_p if macd_signal == 0 and macd_zero_line == 0 else 0
        imp_buy_count += macd_p if macd_signal == 1 and macd_zero_line == 0 else 0
        imp_sell_count += macd_p if macd_signal == 0 and macd_zero_line == 1 else 0

        # Trend
        buy_count += aroon_p if aroon_signal == 1 else 0
        sell_count += aroon_p if aroon_signal == 0 else 0
        hold_count += aroon_p if aroon_signal == 'NA' else 0

        # Imp Indicators
        imp_buy_count += aroon_p if aroon_signal == 1 else 0
        imp_sell_count += aroon_p if aroon_signal == 0 else 0
        imp_hold_count += aroon_p if aroon_signal == 'NA' else 0

        buy_count += ema_p if ema_signal == 1 else 0
        sell_count += ema_p if ema_signal == 0 else 0

        buy_count += wma_p if wma_signal == 1 else 0
        sell_count += wma_p if wma_signal == 0 else 0

        buy_count += sma_p if sma_signal == 1 else 0
        sell_count += sma_p if sma_signal == 0 else 0

        # Volatility
        buy_count += bb_p if bb_signal == 1 else 0
        sell_count += bb_p if bb_signal == 0 else 0
        hold_count += bb_p if bb_signal == 'NA' else 0

        # Imp Indicators
        imp_buy_count += bb_p if bb_signal == 1 else 0
        imp_sell_count += bb_p if bb_signal == 0 else 0
        imp_hold_count += bb_p if bb_signal == 'NA' else 0

        buy_count += adx_p if adx_signal == 1 else 0
        sell_count += adx_p if adx_signal == 0 else 0

        buy_count += kc_p if kc_signal == 1 else 0
        sell_count += kc_p if kc_signal == 0 else 0
        hold_count += kc_p if kc_signal == 'NA' else 0

        buy_count += dc_p if dc_signal == 1 else 0
        sell_count += dc_p if dc_signal == 0 else 0
        hold_count += dc_p if dc_signal == 'NA' else 0

        # Volume
        buy_count += obv_p if obv_signal == 1 else 0
        sell_count += obv_p if obv_signal == 0 else 0
        hold_count += obv_p if obv_signal == 'NA' else 0

        buy_count += cmf_p if cmf_signal == 1 else 0
        sell_count += cmf_p if cmf_signal == 0 else 0
        hold_count += cmf_p if cmf_signal == 'NA' else 0

        buy_count += eom_p if eom_signal == 1 else 0
        sell_count += eom_p if eom_signal == 0 else 0
        hold_count += eom_p if eom_signal == 'NA' else 0

        buy_count += mfi_p if mfi_signal == 1 else 0
        sell_count += mfi_p if mfi_signal == 0 else 0
        hold_count += mfi_p if mfi_signal == 'NA' else 0

        # Determine action IMP indicators
        if imp_buy_count > imp_sell_count and imp_buy_count > imp_hold_count:
            imp_indicators = 1
        elif imp_sell_count > imp_buy_count and imp_sell_count > imp_hold_count:
            imp_indicators = 0
        else:
            imp_indicators = 'NA'

        # Determine action all indicators
        if buy_count > sell_count and buy_count > hold_count:
            all_indicators = 1
        elif sell_count > buy_count and sell_count > hold_count:
            all_indicators = 0
        else:
            all_indicators = 'NA'

        # Determine action for Final Result
        if all_indicators == 1 and imp_indicators == 1:
            final_result = 1
        elif all_indicators == 0 and imp_indicators == 0:
            final_result = 0
        else:
            final_result = 'NA'

        # Return Final Result
        return final_result, buy_count, sell_count, hold_count, imp_buy_count, imp_sell_count, imp_hold_count # 1 Buy, 0 Sell, 'NA' Hold and Signal, Scores

    except Exception as e:
        print(f"An unexpected error occurred in Signal Section: {e}")
