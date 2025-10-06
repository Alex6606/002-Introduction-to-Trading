"""
plotting.py
-----------
Genera las gráficas de resultados del portafolio.
"""

import matplotlib.pyplot as plt
import pandas as pd

def plot_portfolio(port_train, port_test, port_val):
    """
    Muestra la evolución del portafolio durante Train, Test y Validation.
    """
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

    plt.figure(figsize=(12, 6))
    plt.plot(segments["Train"], port_all.loc[segments["Train"]], label="Train", color="blue")
    plt.plot(segments["Test"], port_all.loc[segments["Test"]], label="Test", color="orange")
    plt.plot(segments["Validation"], port_all.loc[segments["Validation"]], label="Validation", color="green")
    plt.title("Evolución del Portafolio (Train → Test → Validation)")
    plt.xlabel("Steps")
    plt.ylabel("Portfolio Value")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.show()
