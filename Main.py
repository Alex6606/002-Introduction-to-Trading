"""
main.py
-------
Punto de entrada del sistema. Orquesta todo el flujo.
"""

from utils import load_data, split_data
from config import DATA_PATH, INITIAL_CAPITAL, COMMISSION, WINDOW_FRAC, STEP_FRAC, N_TRIALS
from backtest import run_backtest
from optimization import walk_forward_optimization
from plotting import plot_portfolio

def main():
    print("🚀 Iniciando pipeline de backtesting y optimización...\n")
    data = load_data(DATA_PATH)
    train, test, validation = split_data(data)

    avg_params, all_params = walk_forward_optimization(train, window_frac=WINDOW_FRAC, step_frac=STEP_FRAC, n_trials=N_TRIALS)
    print("\n✅ Parámetros promedio encontrados:")
    print(avg_params)

    # Evaluación final
    port_train, metrics_train = run_backtest(train, avg_params, INITIAL_CAPITAL, COMMISSION)
    port_test, metrics_test = run_backtest(test, avg_params, INITIAL_CAPITAL, COMMISSION)
    port_val, metrics_val = run_backtest(validation, avg_params, INITIAL_CAPITAL, COMMISSION)

    print("\n📊 RESULTADOS:")
    print("Train:", metrics_train)
    print("Test:", metrics_test)
    print("Validation:", metrics_val)

    plot_portfolio(port_train, port_test, port_val)

if __name__ == "__main__":
    main()
