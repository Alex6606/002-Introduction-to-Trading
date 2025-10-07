"""
plotting.py
-----------
Genera las gráficas de resultados del portafolio.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd



def plot_returns_distribution(portfolio_values):
    """
    Muestra la distribución de los rendimientos del portafolio.

    Args:
        portfolio_values: Series con los valores del portafolio
    """
    # Convertir a DataFrame temporalmente para cálculos
    df_temp = pd.DataFrame({'Value': portfolio_values})
    rets = df_temp['Value'].pct_change().dropna()

    plt.figure(figsize=(8, 5))
    sns.histplot(rets, bins=50, kde=True, color='teal')
    plt.title('Distribución de los Rendimientos')
    plt.xlabel('Rendimiento Diario')
    plt.ylabel('Frecuencia')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()


def plot_portfolio_with_drawdown(port_train, port_test, port_val, figsize=(12, 8)):
    """
    Muestra la evolución del portafolio y drawdown en un solo gráfico con subplots.

    Args:
        port_train: Series con valores de entrenamiento
        port_test: Series con valores de test
        port_val: Series con valores de validation
        figsize: Tamaño de la figura
    """
    # Crear figura con 2 subplots (equity curve arriba, drawdown abajo)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize, sharex=True)

    # ===== PARTE 1: EQUITY CURVE =====
    # Concatenar todas las series
    port_all = pd.concat([
        port_train.reset_index(drop=True).rename("Train"),
        port_test.reset_index(drop=True).rename("Test"),
        port_val.reset_index(drop=True).rename("Validation")
    ])
    port_all.index = range(len(port_all))

    segments = {
        "Train": range(len(port_train)),
        "Test": range(len(port_train), len(port_train) + len(port_test)),
        "Validation": range(len(port_train) + len(port_test), len(port_all))
    }

    # Plotear equity curve
    ax1.plot(segments["Train"], port_all.loc[segments["Train"]], label="Train", color="blue", linewidth=2)
    ax1.plot(segments["Test"], port_all.loc[segments["Test"]], label="Test", color="orange", linewidth=2)
    ax1.plot(segments["Validation"], port_all.loc[segments["Validation"]], label="Validation", color="green",
             linewidth=2)

    # Líneas verticales separadoras
    ax1.axvline(x=len(port_train), color='red', linestyle='--', alpha=0.7, label='Inicio Test')
    ax1.axvline(x=len(port_train) + len(port_test), color='purple', linestyle='--', alpha=0.7,
                label='Inicio Validation')

    ax1.set_title("Evolución del Portafolio (Train → Test → Validation)")
    ax1.set_ylabel("Portfolio Value ($)")
    ax1.legend()
    ax1.grid(True, linestyle="--", alpha=0.6)

    # ===== PARTE 2: DRAWDOWN =====
    # Calcular drawdown para cada segmento
    for segment_name, segment_range in segments.items():
        segment_values = port_all.loc[segment_range]
        df_temp = pd.DataFrame({'Value': segment_values})
        cummax = df_temp['Value'].cummax()
        drawdown = (df_temp['Value'] - cummax) / cummax

        # Plotear drawdown con el mismo color que la equity curve
        color = {"Train": "blue", "Test": "orange", "Validation": "green"}[segment_name]
        ax2.fill_between(segment_range, drawdown, color=color, alpha=0.5, label=f'{segment_name} Drawdown')

    ax2.set_title('Drawdown del Portafolio')
    ax2.set_xlabel('Tiempo / Steps')
    ax2.set_ylabel('Drawdown (%)')
    ax2.legend()
    ax2.grid(True, linestyle='--', alpha=0.6)
    ax2.set_ylim(bottom=min(ax2.get_ylim()[0], -0.1))  # Asegurar que se vea bien el drawdown

    plt.tight_layout()
    plt.show()


# Versión alternativa para una sola serie (compatibilidad)
def plot_single_portfolio_with_drawdown(portfolio_values, title="Portafolio y Drawdown"):
    """
    Versión para una sola serie de portfolio.

    Args:
        portfolio_values: Series con los valores del portafolio
        title: Título del gráfico
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    # Equity curve
    ax1.plot(portfolio_values.index, portfolio_values.values,
             label='Portfolio Value', color='blue', linewidth=2)
    ax1.set_title(f"{title} - Equity Curve")
    ax1.set_ylabel("Portfolio Value ($)")
    ax1.legend()
    ax1.grid(True, linestyle="--", alpha=0.6)

    # Drawdown
    df_temp = pd.DataFrame({'Value': portfolio_values})
    cummax = df_temp['Value'].cummax()
    drawdown = (df_temp['Value'] - cummax) / cummax

    ax2.fill_between(portfolio_values.index, drawdown, color='tomato', alpha=0.5, label='Drawdown')
    ax2.set_title('Drawdown')
    ax2.set_xlabel('Tiempo')
    ax2.set_ylabel('Drawdown (%)')
    ax2.legend()
    ax2.grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout()
    plt.show()


def plot_signals_continuous(df_train, df_test, df_val, figsize=(15, 6)):
    """
    Grafica las señales de forma continua concatenando train, test y validation.

    Args:
        df_train: DataFrame con datos de entrenamiento
        df_test: DataFrame con datos de test
        df_val: DataFrame con datos de validation
        figsize: Tamaño de la figura
    """
    # Concatenar todos los datos
    df_all = pd.concat([df_train, df_test, df_val])
    df_all.index = range(len(df_all))

    # Definir los límites de cada segmento
    train_end = len(df_train)
    test_end = train_end + len(df_test)

    plt.figure(figsize=figsize)

    # Plot del precio completo
    plt.plot(df_all['Close'], label='Precio', color='black', alpha=0.6, linewidth=1)

    # Señales de compra
    buy_signals = df_all[df_all['buy_signal']]
    if not buy_signals.empty:
        plt.scatter(buy_signals.index, buy_signals['Close'],
                    marker='^', color='green', label='Compra', s=50, alpha=0.8)

    # Señales de venta
    sell_signals = df_all[df_all['sell_signal']]
    if not sell_signals.empty:
        plt.scatter(sell_signals.index, sell_signals['Close'],
                    marker='v', color='red', label='Venta', s=50, alpha=0.8)

    # Líneas verticales para separar las fases
    plt.axvline(x=train_end, color='blue', linestyle='--', alpha=0.7, label='Fin Train')
    plt.axvline(x=test_end, color='orange', linestyle='--', alpha=0.7, label='Fin Test')

    # Áreas sombreadas para cada fase
    plt.axvspan(0, train_end, alpha=0.1, color='blue', label='Train')
    plt.axvspan(train_end, test_end, alpha=0.1, color='orange', label='Test')
    plt.axvspan(test_end, len(df_all), alpha=0.1, color='green', label='Validation')

    plt.title('SEÑALES DE COMPRA/VENTA - Train → Test → Validation')
    plt.xlabel('Tiempo')
    plt.ylabel('Precio')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

