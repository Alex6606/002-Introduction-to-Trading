"""
utils.py
--------
Funciones auxiliares para carga de datos y cálculos generales.
"""

import pandas as pd

def load_data(path: str) -> pd.DataFrame:
    """
    Carga el archivo CSV y prepara la columna de fecha.
    """
    data = pd.read_csv(path, header=1).dropna()
    data = data.sort_values('Date').reset_index(drop=True)
    return data

def split_data(data: pd.DataFrame, train_frac=0.6, test_frac=0.2):
    """
    Divide los datos en train, test y validation.
    """
    n = len(data)
    train_size = int(train_frac * n)
    test_size = int(test_frac * n)

    train = data.iloc[:train_size]
    test = data.iloc[train_size:train_size + test_size]
    validation = data.iloc[train_size + test_size:]

    return train, test, validation
