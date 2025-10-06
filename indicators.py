"""
Módulo para cálculo de indicadores técnicos.
"""
import pandas as pd
import ta


class TechnicalIndicators:
    """Clase para calcular indicadores técnicos."""

    @staticmethod
    def calculate_rsi(df: pd.DataFrame, window: int) -> pd.DataFrame:
        """
        Calcula RSI y señales.

        Args:
            df: DataFrame con datos
            window: Ventana del RSI

        Returns:
            DataFrame con columnas RSI añadidas
        """
        rsi_indicator = ta.momentum.RSIIndicator(df['Close'], window=window)
        df = df.copy()
        df['rsi'] = rsi_indicator.rsi()
        return df

    @staticmethod
    def calculate_macd(df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcula MACD y señales.

        Args:
            df: DataFrame con datos

        Returns:
            DataFrame con columnas MACD añadidas
        """
        macd = ta.trend.MACD(df['Close'])
        df = df.copy()
        df['macd'] = macd.macd()
        df['macd_signal'] = macd.macd_signal()
        return df

    @staticmethod
    def calculate_ema(df: pd.DataFrame, fast: int, slow: int) -> pd.DataFrame:
        """
        Calcula EMAs y señales.

        Args:
            df: DataFrame con datos
            fast: Periodo EMA rápida
            slow: Periodo EMA lenta

        Returns:
            DataFrame con columnas EMA añadidas
        """
        df = df.copy()
        df['ema_fast'] = ta.trend.EMAIndicator(df['Close'], window=fast).ema_indicator()
        df['ema_slow'] = ta.trend.EMAIndicator(df['Close'], window=slow).ema_indicator()
        return df

    @staticmethod
    def generate_signals(df: pd.DataFrame, rsi_lower: int) -> pd.DataFrame:
        """
        Genera señales de trading basadas en indicadores.

        Args:
            df: DataFrame con indicadores calculados
            rsi_lower: Límite inferior del RSI

        Returns:
            DataFrame con señales añadidas
        """
        df = df.copy()

        # Señales individuales
        df['signal_rsi_long'] = df['rsi'] < rsi_lower
        df['signal_rsi_short'] = df['rsi'] > (100 - rsi_lower)
        df['signal_macd_long'] = df['macd'] > df['macd_signal']
        df['signal_macd_short'] = df['macd'] < df['macd_signal']
        df['signal_ema_long'] = df['ema_fast'] > df['ema_slow']
        df['signal_ema_short'] = df['ema_fast'] < df['ema_slow']

        # Reglas 2 de 3
        df['buy_signal'] = (
                df[['signal_rsi_long', 'signal_macd_long', 'signal_ema_long']].sum(axis=1) >= 2
        )
        df['sell_signal'] = (
                df[['signal_rsi_short', 'signal_macd_short', 'signal_ema_short']].sum(axis=1) >= 2
        )

        return df