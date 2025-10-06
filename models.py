"""
models.py
---------
Define estructuras de datos (dataclasses) utilizadas en el backtest.
"""

from dataclasses import dataclass

@dataclass
class Position:
    """
    Representa una posición abierta (long o short).
    """
    ticker: str
    n_shares: float
    price: float
    sl: float
    tp: float
    time: str
    direction: str
