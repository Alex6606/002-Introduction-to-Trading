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
WINDOW_FRAC = 0.6
STEP_FRAC = 0.1
N_TRIALS = 10
