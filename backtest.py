"""
backtest.py
------------
Contiene la lógica de la estrategia y simulación del portafolio.
"""

import numpy as np
import pandas as pd
import ta
from models import Position

def get_portfolio_value(capital, active_positions, current_price, com):
    """
    Calcula el valor total del portafolio (capital + posiciones abiertas).
    """
    value = capital
    for pos in active_positions:
        if pos.direction == "long":
            value += pos.n_shares * current_price
        elif pos.direction == "short":
            value += (pos.price * pos.n_shares) + (pos.n_shares * pos.price - current_price * pos.n_shares) * (1 - com)
    return value

def run_backtest(data, params, initial_capital, com):
    """
    Corre backtest en base a RSI, MACD y EMA con reglas 2 de 3.
    """
    # === Extraer parámetros ===
    rsi_window = params["rsi_window"]
    rsi_lower = params["rsi_lower"]
    ema_fast = params["ema_fast"]
    ema_slow = params["ema_slow"]
    stop_loss = params["stop_loss"]
    take_profit = params["take_profit"]
    n_shares = params["n_shares"]

    df = data.copy()

    from indicators import add_indicators
    df = add_indicators(df,rsi_window,rsi_lower, ema_fast, ema_slow)

    # === Backtest ===
    active_positions = []
    capital = initial_capital
    portfolio_values = [capital]

    for _, row in df.iterrows():
        # Cierre de posiciones
        for pos in active_positions.copy():
            if pos.direction == "long" and (row.Close >= pos.tp or row.Close <= pos.sl):
                capital += row.Close * pos.n_shares * (1 - com)
                active_positions.remove(pos)
            elif pos.direction == "short" and (row.Close <= pos.tp or row.Close >= pos.sl):
                capital += ((pos.price * pos.n_shares) + (pos.price * n_shares - row.Close * pos.n_shares)) * (1 - com)
                active_positions.remove(pos)

        # Apertura LONG
        if row.buy_signal and not any(p.direction == "long" for p in active_positions):
            cost = row.Close * n_shares * (1 + com)
            if capital > cost:
                capital -= cost
                active_positions.append(Position("BTCUSDT", n_shares, row.Close,
                                                 row.Close*(1-stop_loss), row.Close*(1+take_profit),
                                                 row.Date, "long"))

        # Apertura SHORT
        elif row.sell_signal and not any(p.direction == "short" for p in active_positions):
            cost = row.Close * n_shares * (1 - com)
            if capital > cost:
                capital -= cost
                active_positions.append(Position("BTCUSDT", n_shares, row.Close,
                                                 row.Close*(1+stop_loss), row.Close*(1-take_profit),
                                                 row.Date, "short"))

        portfolio_values.append(get_portfolio_value(capital, active_positions, row.Close, com))

    # Cerrar posiciones restantes
    for pos in active_positions:
        pnl = (row.Close - pos.price) * pos.n_shares if pos.direction == "long" else (pos.price - row.Close) * pos.n_shares
        capital += pnl * (1 - com)

    df_portfolio = pd.DataFrame({'Value': portfolio_values})
    df_portfolio['rets'] = df_portfolio['Value'].pct_change().dropna()

    rets = df_portfolio['rets']
    mean, std, down_risk = rets.mean(), rets.std(), rets[rets < 0].std()
    scale = 24 * 365
    annual_rets = mean * scale
    annual_std = std * np.sqrt(scale)
    annual_down_risk = down_risk * np.sqrt(scale)
    sharpe = annual_rets / annual_std if annual_std else 0
    sortino = annual_rets / annual_down_risk if annual_down_risk else 0
    cummax = df_portfolio['Value'].cummax()
    drawdown = (df_portfolio['Value'] - cummax) / cummax
    max_dd = drawdown.min()
    calmar = annual_rets / abs(max_dd) if max_dd else 0

    metrics = {
        "Sharpe": sharpe, "Sortino": sortino, "Calmar": calmar,
        "MaxDrawdown": max_dd, "AnnualReturn": annual_rets,
        "WinRate": (rets > 0).sum() / len(rets) if len(rets) else 0
    }

    return df_portfolio['Value'], metrics, df
