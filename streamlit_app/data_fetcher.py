"""
Data fetcher module using yfinance for stock data.
"""
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, Dict, Any


class DataFetcher:
    """Fetches stock data using yfinance."""
    
    def __init__(self, ticker: str):
        """
        Initialize data fetcher.
        
        Args:
            ticker: Stock ticker symbol (e.g., 'AAPL')
        """
        self.ticker = ticker.upper()
        self.stock = None
        self.info = None
        
    def fetch_data(self, timeframe: str = "short") -> Optional[pd.DataFrame]:
        """
        Fetch historical stock data based on timeframe.
        
        Args:
            timeframe: 'short', 'medium', or 'long'
            
        Returns:
            DataFrame with OHLCV data or None if error
        """
        try:
            self.stock = yf.Ticker(self.ticker)
            
            # Determine period based on timeframe
            period_map = {
                "short": "60d",    # 60 days for short-term (need history for indicators)
                "medium": "6mo",   # 6 months for medium-term
                "long": "2y"       # 2 years for long-term
            }
            
            period = period_map.get(timeframe, "60d")
            
            # Fetch data
            data = self.stock.history(period=period)
            
            if data.empty:
                return None
                
            return data
            
        except Exception as e:
            print(f"Error fetching data for {self.ticker}: {e}")
            return None
    
    def get_stock_info(self) -> Dict[str, Any]:
        """
        Get stock information (company name, price, etc.).
        
        Returns:
            Dictionary with stock info
        """
        try:
            if self.stock is None:
                self.stock = yf.Ticker(self.ticker)
            
            info = self.stock.info
            
            # Extract relevant info
            return {
                'name': info.get('longName', self.ticker),
                'current_price': info.get('currentPrice', info.get('regularMarketPrice', 0)),
                'previous_close': info.get('previousClose', 0),
                'volume': info.get('volume', 0),
                'avg_volume': info.get('averageVolume', 0),
                'market_cap': info.get('marketCap', 0),
                'pe_ratio': info.get('trailingPE', 0),
                'eps': info.get('trailingEps', 0),
                'profit_margin': info.get('profitMargins', 0),
                'revenue_growth': info.get('revenueGrowth', 0),
            }
            
        except Exception as e:
            print(f"Error getting stock info: {e}")
            return {
                'name': self.ticker,
                'current_price': 0,
                'previous_close': 0,
                'volume': 0,
                'avg_volume': 0,
                'market_cap': 0,
                'pe_ratio': 0,
                'eps': 0,
                'profit_margin': 0,
                'revenue_growth': 0,
            }
    
    def validate_ticker(self) -> bool:
        """
        Validate if ticker exists and has data.
        
        Returns:
            True if valid, False otherwise
        """
        try:
            stock = yf.Ticker(self.ticker)
            info = stock.info
            
            # Check if we got valid data
            if 'regularMarketPrice' in info or 'currentPrice' in info:
                return True
            return False
            
        except:
            return False
