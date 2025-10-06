"""
Módulo para gestión de portafolio y posiciones.
"""
from config import Position, BacktestMetrics
import pandas as pd
import numpy as np


class PortfolioManager:
    """Clase para gestionar el portafolio y calcular métricas."""

    @staticmethod
    def get_portfolio_value(capital: float, active_positions: list, current_price: float, com: float) -> float:
        """
        Calcula el valor total del portafolio.

        Args:
            capital: Capital libre
            active_positions: Lista de posiciones activas
            current_price: Precio actual del activo
            com: Comisión por trade

        Returns:
            Valor total del portafolio
        """
        value = capital
        for pos in active_positions:
            if pos.direction == "long":
                value += pos.n_shares * current_price
            elif pos.direction == "short":
                value += (pos.price * pos.n_shares) + \
                         (pos.n_shares * pos.price - current_price * pos.n_shares) * (1 - com)
        return value

    @staticmethod
    def calculate_metrics(portfolio_values: pd.Series) -> BacktestMetrics:
        """
        Calcula métricas de performance del backtest.

        Args:
            portfolio_values: Serie con evolución del portafolio

        Returns:
            Objeto BacktestMetrics con las métricas
        """
        df_portfolio = pd.DataFrame()
        df_portfolio['Value'] = portfolio_values
        df_portfolio['rets'] = df_portfolio.Value.pct_change().dropna()

        rets = df_portfolio['rets']
        mean = rets.mean()
        std = rets.std()
        down_risk = rets[rets < 0].std()

        scale = 24 * 365
        annual_rets = mean * scale
        annual_std = std * np.sqrt(scale)
        annual_down_risk = down_risk * np.sqrt(scale)

        sharpe = annual_rets / annual_std if annual_std != 0 else 0
        sortino = annual_rets / annual_down_risk if annual_down_risk != 0 else 0

        cummax = df_portfolio['Value'].cummax()
        drawdown = (df_portfolio['Value'] - cummax) / cummax
        max_dd = drawdown.min()
        calmar = abs(annual_rets / max_dd) if max_dd != 0 else 0

        return BacktestMetrics(
            Sharpe=sharpe,
            Sortino=sortino,
            Calmar=calmar,
            MaxDrawdown=max_dd,
            AnnualReturn=annual_rets,
            WinRate=(rets > 0).sum() / len(rets) if len(rets) > 0 else 0
        )