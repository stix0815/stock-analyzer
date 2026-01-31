"""
Technical indicators calculation module.
"""
import pandas as pd
import numpy as np
from typing import Dict, Any


class TechnicalIndicators:
    """Calculate technical indicators for stock analysis."""
    
    def __init__(self, data: pd.DataFrame):
        """
        Initialize with price data.
        
        Args:
            data: DataFrame with OHLCV data
        """
        self.data = data.copy()
        self.indicators = {}
        
    def calculate_all(self) -> Dict[str, Any]:
        """
        Calculate all technical indicators.
        
        Returns:
            Dictionary with all calculated indicators
        """
        self.calculate_rsi()
        self.calculate_macd()
        self.calculate_bollinger_bands()
        self.calculate_sma()
        self.calculate_volume_metrics()
        
        return self.indicators
    
    def calculate_rsi(self, period: int = 14) -> float:
        """
        Calculate RSI (Relative Strength Index).
        
        Args:
            period: RSI period (default 14)
            
        Returns:
            Current RSI value
        """
        close = self.data['Close']
        delta = close.diff()
        
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        current_rsi = rsi.iloc[-1]
        
        self.indicators['rsi'] = {
            'value': current_rsi,
            'series': rsi,
            'signal': self._interpret_rsi(current_rsi)
        }
        
        return current_rsi
    
    def _interpret_rsi(self, rsi: float) -> str:
        """Interpret RSI signal."""
        if rsi < 30:
            return "OVERSOLD"
        elif rsi > 70:
            return "OVERBOUGHT"
        else:
            return "NEUTRAL"
    
    def calculate_macd(self, fast: int = 12, slow: int = 26, signal: int = 9):
        """
        Calculate MACD (Moving Average Convergence Divergence).
        
        Args:
            fast: Fast EMA period
            slow: Slow EMA period
            signal: Signal line period
        """
        close = self.data['Close']
        
        ema_fast = close.ewm(span=fast, adjust=False).mean()
        ema_slow = close.ewm(span=slow, adjust=False).mean()
        
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal, adjust=False).mean()
        histogram = macd_line - signal_line
        
        self.indicators['macd'] = {
            'macd_line': macd_line.iloc[-1],
            'signal_line': signal_line.iloc[-1],
            'histogram': histogram.iloc[-1],
            'macd_series': macd_line,
            'signal_series': signal_line,
            'histogram_series': histogram,
            'signal': self._interpret_macd(macd_line.iloc[-1], signal_line.iloc[-1], 
                                           histogram.iloc[-1], histogram.iloc[-2])
        }
    
    def _interpret_macd(self, macd: float, signal: float, hist: float, prev_hist: float) -> str:
        """Interpret MACD signal."""
        if macd > signal and hist > prev_hist:
            return "BULLISH"
        elif macd < signal and hist < prev_hist:
            return "BEARISH"
        else:
            return "NEUTRAL"
    
    def calculate_bollinger_bands(self, period: int = 20, std_dev: int = 2):
        """
        Calculate Bollinger Bands.
        
        Args:
            period: Moving average period
            std_dev: Number of standard deviations
        """
        close = self.data['Close']
        
        sma = close.rolling(window=period).mean()
        std = close.rolling(window=period).std()
        
        upper_band = sma + (std * std_dev)
        lower_band = sma - (std * std_dev)
        
        current_price = close.iloc[-1]
        
        self.indicators['bollinger'] = {
            'upper': upper_band.iloc[-1],
            'middle': sma.iloc[-1],
            'lower': lower_band.iloc[-1],
            'current': current_price,
            'upper_series': upper_band,
            'middle_series': sma,
            'lower_series': lower_band,
            'signal': self._interpret_bollinger(current_price, upper_band.iloc[-1], 
                                                lower_band.iloc[-1], sma.iloc[-1])
        }
    
    def _interpret_bollinger(self, price: float, upper: float, lower: float, middle: float) -> str:
        """Interpret Bollinger Bands signal."""
        if price <= lower:
            return "NEAR LOWER BAND (oversold)"
        elif price >= upper:
            return "NEAR UPPER BAND (overbought)"
        elif price < middle:
            return "BELOW MIDDLE (bearish)"
        else:
            return "ABOVE MIDDLE (bullish)"
    
    def calculate_sma(self, short_period: int = 50, long_period: int = 200):
        """
        Calculate Simple Moving Averages.
        
        Args:
            short_period: Short-term SMA period
            long_period: Long-term SMA period
        """
        close = self.data['Close']
        
        sma_50 = close.rolling(window=short_period).mean()
        sma_200 = close.rolling(window=long_period).mean()
        
        current_price = close.iloc[-1]
        
        self.indicators['sma'] = {
            'sma_50': sma_50.iloc[-1] if len(sma_50) >= short_period else None,
            'sma_200': sma_200.iloc[-1] if len(sma_200) >= long_period else None,
            'current': current_price,
            'sma_50_series': sma_50,
            'sma_200_series': sma_200,
            'signal': self._interpret_sma(current_price, 
                                         sma_50.iloc[-1] if len(sma_50) >= short_period else None,
                                         sma_200.iloc[-1] if len(sma_200) >= long_period else None)
        }
    
    def _interpret_sma(self, price: float, sma_50: float, sma_200: float) -> str:
        """Interpret SMA signal."""
        if sma_50 is None or sma_200 is None:
            return "INSUFFICIENT DATA"
        
        if price > sma_50 and sma_50 > sma_200:
            return "STRONG UPTREND (Golden Cross)"
        elif price < sma_50 and sma_50 < sma_200:
            return "STRONG DOWNTREND (Death Cross)"
        elif price > sma_200:
            return "ABOVE 200-day (bullish long-term)"
        elif price < sma_200:
            return "BELOW 200-day (bearish long-term)"
        else:
            return "NEUTRAL"
    
    def calculate_volume_metrics(self, period: int = 20):
        """
        Calculate volume metrics.
        
        Args:
            period: Period for average volume
        """
        volume = self.data['Volume']
        
        avg_volume = volume.rolling(window=period).mean()
        current_volume = volume.iloc[-1]
        avg_vol = avg_volume.iloc[-1]
        
        volume_change_pct = ((current_volume - avg_vol) / avg_vol) * 100 if avg_vol > 0 else 0
        
        self.indicators['volume'] = {
            'current': current_volume,
            'average': avg_vol,
            'change_pct': volume_change_pct,
            'series': volume,
            'avg_series': avg_volume,
            'signal': self._interpret_volume(volume_change_pct)
        }
    
    def _interpret_volume(self, change_pct: float) -> str:
        """Interpret volume signal."""
        if change_pct > 50:
            return "VERY HIGH VOLUME (strong confirmation)"
        elif change_pct > 20:
            return "ELEVATED VOLUME (confirmation)"
        elif change_pct < -20:
            return "LOW VOLUME (weak signal)"
        else:
            return "NORMAL VOLUME"
