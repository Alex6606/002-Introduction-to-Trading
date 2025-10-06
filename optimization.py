"""
optimization.py
---------------
Contiene la lógica de Optuna y Walk-Forward Optimization.
"""

import numpy as np
import optuna
from backtest import run_backtest

def optimize_parameters(train_w, valid_w, n_trials=15):
    """
    Optuna: optimiza parámetros para una ventana.
    """
    def objective(trial):
        params = {
            "rsi_window": trial.suggest_int("rsi_window", 5, 30),
            "rsi_lower": trial.suggest_int("rsi_lower", 20, 35),
            "ema_fast": trial.suggest_int("ema_fast", 5, 20),
            "ema_slow": trial.suggest_int("ema_slow", 30, 100),
            "stop_loss": trial.suggest_float("stop_loss", 0.01, 0.15),
            "take_profit": trial.suggest_float("take_profit", 0.01, 0.15),
            "n_shares": trial.suggest_float("n_shares", 0.001, 5),
        }

        _, m_train = run_backtest(train_w, params, 1_000_000, 0.00125)
        _, m_valid = run_backtest(valid_w, params, 1_000_000, 0.00125)
        return 0.7 * m_train["Calmar"] + 0.3 * m_valid["Calmar"]

    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=n_trials, show_progress_bar=False)
    return study.best_params

def walk_forward_optimization(data, window_frac=0.4, step_frac=0.1, n_trials=15):
    """
    Walk-Forward promediado con Optuna.
    """
    n = len(data)
    window_size = int(n * window_frac)
    step_size = int(n * step_frac)
    param_list = []

    for start in range(0, n - window_size, step_size):
        window = data.iloc[start:start + window_size]
        train_w = window.iloc[:int(0.7 * len(window))]
        valid_w = window.iloc[int(0.7 * len(window)):]
        best_params = optimize_parameters(train_w, valid_w, n_trials)
        param_list.append(best_params)

    avg_params = {k: np.mean([p[k] for p in param_list]) for k in param_list[0]}
    return avg_params, param_list
