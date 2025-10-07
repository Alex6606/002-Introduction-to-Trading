import pandas as pd
import ta  # Technical Analysis library

def add_indicators(df, rsi_window=14, rsi_lower=30, ema_fast=12, ema_slow=26 ,bb_window=20, bb_n_std=2 ):
    # === RSI ===
    df['rsi'] = ta.momentum.RSIIndicator(df['Close'], window=rsi_window).rsi()
    df['signal_rsi_long'] = df['rsi'] < rsi_lower
    df['signal_rsi_short'] = df['rsi'] > (100 - rsi_lower)

    # === MACD ===
    macd = ta.trend.MACD(df['Close'])
    df['signal_macd_long'] = macd.macd() > macd.macd_signal()
    df['signal_macd_short'] = macd.macd() < macd.macd_signal()

    # === EMA Fast / Slow ===
    df['ema_fast'] = ta.trend.EMAIndicator(df['Close'], window=ema_fast).ema_indicator()
    df['ema_slow'] = ta.trend.EMAIndicator(df['Close'], window=ema_slow).ema_indicator()
    df['signal_ema_long'] = df['ema_fast'] > df['ema_slow']
    df['signal_ema_short'] = df['ema_fast'] < df['ema_slow']

    # === Señales combinadas ===
    df['buy_signal'] = (
        df[['signal_rsi_long', 'signal_macd_long', 'signal_ema_long']].sum(axis=1) >= 2
    )
    df['sell_signal'] = (
        df[['signal_rsi_short', 'signal_macd_short', 'signal_ema_short']].sum(axis=1) >= 2
    )

    df = df.dropna()
    return df
