"""
config.py
---------
Contiene configuraciones globales, rutas y constantes.
"""

# Parámetros del dataset
DATA_PATH = "Binance_BTCUSDT_1h.csv"

# Backtest
INITIAL_CAPITAL = 1_000_000
COMMISSION = 0.125 / 100

# Walk-forward optimization
WINDOW_FRAC = 0.7
STEP_FRAC = 0.1
N_TRIALS = 100

# Mejores Parametros encontrados:
MEJORES_PARAMS_INT = {
    'rsi_window': 11,
    'rsi_lower': 26,
    'ema_fast': 7,
    'ema_slow': 85,
    'stop_loss': 0.044,
    'take_profit': 0.107,
    'n_shares': 2.71
}
