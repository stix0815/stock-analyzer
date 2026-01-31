"""
Scoring system for stock analysis based on technical indicators.
"""
from typing import Dict, Any, Tuple


class ScoringSystem:
    """Score stocks based on technical indicators and timeframe."""
    
    # Scoring weights by timeframe (from FINAL_SPEC.md)
    WEIGHTS = {
        'short': {
            'rsi': 25,
            'macd': 30,
            'bollinger': 20,
            'volume': 15,
            'sma': 10
        },
        'medium': {
            'macd': 25,
            'sma': 25,
            'rsi': 20,
            'bollinger': 15,
            'volume': 10,
            'sentiment': 5
        },
        'long': {
            'sma': 30,
            'fundamentals': 25,
            'sec_filings': 15,
            'macd': 15,
            'rsi': 10,
            'sentiment': 5
        }
    }
    
    def __init__(self, timeframe: str, risk_tolerance: str):
        """
        Initialize scoring system.
        
        Args:
            timeframe: 'short', 'medium', or 'long'
            risk_tolerance: 'conservative', 'moderate', or 'aggressive'
        """
        self.timeframe = timeframe
        self.risk_tolerance = risk_tolerance
        self.weights = self.WEIGHTS.get(timeframe, self.WEIGHTS['short'])
        
    def calculate_score(self, indicators: Dict[str, Any], stock_info: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Calculate overall score based on indicators.
        
        Args:
            indicators: Dictionary of calculated indicators
            stock_info: Stock information for fundamentals (optional)
            
        Returns:
            Dictionary with score, signal, and breakdown
        """
        scores = {}
        total_score = 0
        max_score = 0
        
        # RSI scoring
        if 'rsi' in indicators and 'rsi' in self.weights:
            rsi_score = self._score_rsi(indicators['rsi'])
            weight = self.weights['rsi']
            scores['rsi'] = {'score': rsi_score, 'max': weight, 'weighted': (rsi_score / 100) * weight}
            total_score += scores['rsi']['weighted']
            max_score += weight
        
        # MACD scoring
        if 'macd' in indicators and 'macd' in self.weights:
            macd_score = self._score_macd(indicators['macd'])
            weight = self.weights['macd']
            scores['macd'] = {'score': macd_score, 'max': weight, 'weighted': (macd_score / 100) * weight}
            total_score += scores['macd']['weighted']
            max_score += weight
        
        # Bollinger Bands scoring
        if 'bollinger' in indicators and 'bollinger' in self.weights:
            bb_score = self._score_bollinger(indicators['bollinger'])
            weight = self.weights['bollinger']
            scores['bollinger'] = {'score': bb_score, 'max': weight, 'weighted': (bb_score / 100) * weight}
            total_score += scores['bollinger']['weighted']
            max_score += weight
        
        # SMA scoring
        if 'sma' in indicators and 'sma' in self.weights:
            sma_score = self._score_sma(indicators['sma'])
            weight = self.weights['sma']
            scores['sma'] = {'score': sma_score, 'max': weight, 'weighted': (sma_score / 100) * weight}
            total_score += scores['sma']['weighted']
            max_score += weight
        
        # Volume scoring
        if 'volume' in indicators and 'volume' in self.weights:
            vol_score = self._score_volume(indicators['volume'])
            weight = self.weights['volume']
            scores['volume'] = {'score': vol_score, 'max': weight, 'weighted': (vol_score / 100) * weight}
            total_score += scores['volume']['weighted']
            max_score += weight
        
        # Fundamentals scoring (long-term only)
        if self.timeframe == 'long' and stock_info:
            fund_score = self._score_fundamentals(stock_info)
            weight = self.weights.get('fundamentals', 0)
            scores['fundamentals'] = {'score': fund_score, 'max': weight, 'weighted': (fund_score / 100) * weight}
            total_score += scores['fundamentals']['weighted']
            max_score += weight
        
        # Calculate final score (0-100)
        final_score = int(total_score) if max_score > 0 else 0
        
        # Determine signal
        signal, confidence = self._determine_signal(final_score, scores)
        
        return {
            'score': final_score,
            'signal': signal,
            'confidence': confidence,
            'breakdown': scores,
            'max_score': max_score
        }
    
    def _score_rsi(self, rsi_data: Dict) -> int:
        """Score RSI (0-100)."""
        rsi = rsi_data['value']
        
        if rsi < 30:
            return 85  # Oversold - strong buy signal
        elif rsi < 40:
            return 70  # Approaching oversold
        elif rsi < 50:
            return 55  # Slightly bearish
        elif rsi < 60:
            return 50  # Neutral
        elif rsi < 70:
            return 45  # Slightly bullish
        elif rsi < 80:
            return 30  # Approaching overbought
        else:
            return 15  # Overbought - sell signal
    
    def _score_macd(self, macd_data: Dict) -> int:
        """Score MACD (0-100)."""
        macd = macd_data['macd_line']
        signal = macd_data['signal_line']
        histogram = macd_data['histogram']
        
        # MACD above signal = bullish
        if macd > signal:
            if histogram > 0:
                return 85  # Strong bullish
            else:
                return 65  # Bullish but weakening
        else:
            if histogram < 0:
                return 15  # Strong bearish
            else:
                return 35  # Bearish but improving
    
    def _score_bollinger(self, bb_data: Dict) -> int:
        """Score Bollinger Bands (0-100)."""
        price = bb_data['current']
        upper = bb_data['upper']
        lower = bb_data['lower']
        middle = bb_data['middle']
        
        # Calculate position within bands
        band_width = upper - lower
        if band_width == 0:
            return 50
        
        position = (price - lower) / band_width
        
        if position < 0.1:
            return 80  # Near lower band - oversold
        elif position < 0.3:
            return 65  # Below middle
        elif position < 0.5:
            return 50  # Around middle (bearish side)
        elif position < 0.7:
            return 50  # Around middle (bullish side)
        elif position < 0.9:
            return 35  # Above middle
        else:
            return 20  # Near upper band - overbought
    
    def _score_sma(self, sma_data: Dict) -> int:
        """Score SMA (0-100)."""
        price = sma_data['current']
        sma_50 = sma_data['sma_50']
        sma_200 = sma_data['sma_200']
        
        if sma_50 is None or sma_200 is None:
            return 50  # Neutral if insufficient data
        
        # Golden cross (50 > 200, price > 50)
        if price > sma_50 and sma_50 > sma_200:
            return 90
        # Price > 200 but < 50
        elif price > sma_200 and price < sma_50:
            return 60
        # Death cross (50 < 200, price < 50)
        elif price < sma_50 and sma_50 < sma_200:
            return 10
        # Price < 200 but > 50
        elif price < sma_200 and price > sma_50:
            return 40
        else:
            return 50
    
    def _score_volume(self, vol_data: Dict) -> int:
        """Score volume (0-100)."""
        change_pct = vol_data['change_pct']
        
        if change_pct > 50:
            return 90  # Very high volume
        elif change_pct > 20:
            return 75  # Elevated volume
        elif change_pct > 0:
            return 55  # Above average
        elif change_pct > -20:
            return 45  # Slightly below average
        else:
            return 30  # Low volume
    
    def _score_fundamentals(self, stock_info: Dict) -> int:
        """Score fundamentals (0-100) for long-term analysis."""
        score = 50  # Start neutral
        
        # P/E ratio (lower is better, but not too low)
        pe = stock_info.get('pe_ratio', 0)
        if pe > 0:
            if pe < 15:
                score += 15
            elif pe < 25:
                score += 10
            elif pe < 35:
                score += 0
            else:
                score -= 10
        
        # Profit margin
        margin = stock_info.get('profit_margin', 0)
        if margin > 0.20:
            score += 15
        elif margin > 0.10:
            score += 10
        elif margin > 0.05:
            score += 5
        
        # Revenue growth
        growth = stock_info.get('revenue_growth', 0)
        if growth > 0.15:
            score += 20
        elif growth > 0.05:
            score += 10
        elif growth < -0.05:
            score -= 10
        
        return max(0, min(100, score))
    
    def _determine_signal(self, score: int, breakdown: Dict) -> Tuple[str, str]:
        """
        Determine BUY/SELL/HOLD signal and confidence.
        
        Returns:
            Tuple of (signal, confidence)
        """
        # Adjust thresholds based on risk tolerance
        if self.risk_tolerance == 'conservative':
            buy_threshold = 75
            sell_threshold = 30
            confidence_threshold = 70
        elif self.risk_tolerance == 'aggressive':
            buy_threshold = 60
            sell_threshold = 45
            confidence_threshold = 55
        else:  # moderate
            buy_threshold = 65
            sell_threshold = 35
            confidence_threshold = 60
        
        # Determine signal
        if score >= 80:
            signal = "STRONG BUY"
        elif score >= buy_threshold:
            signal = "BUY"
        elif score >= 45 and score <= 55:
            signal = "HOLD"
        elif score <= sell_threshold:
            signal = "SELL"
        elif score <= 20:
            signal = "STRONG SELL"
        else:
            signal = "HOLD"
        
        # Determine confidence based on score and agreement between indicators
        if score >= confidence_threshold or score <= (100 - confidence_threshold):
            confidence = "High"
        elif score >= 55 or score <= 45:
            confidence = "Medium"
        else:
            confidence = "Low"
        
        return signal, confidence
