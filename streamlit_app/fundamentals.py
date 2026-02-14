"""
Fundamental Analysis Module
Fetches and analyzes fundamental metrics for long-term investment strategies.
"""
import yfinance as yf
from typing import Dict, Any, Optional, Tuple
from datetime import datetime


class FundamentalAnalyzer:
    """Analyzes fundamental metrics for stocks."""
    
    def __init__(self, ticker: str):
        """
        Initialize fundamental analyzer.
        
        Args:
            ticker: Stock ticker symbol (e.g., 'AAPL')
        """
        self.ticker = ticker.upper()
        self.stock = yf.Ticker(self.ticker)
        self.info = None
        
    def fetch_fundamentals(self) -> Dict[str, Any]:
        """
        Fetch all fundamental data from yfinance.
        
        Returns:
            Dictionary containing all fundamental metrics organized by category
        """
        try:
            self.info = self.stock.info
            
            fundamentals = {
                'valuation': self._get_valuation_metrics(),
                'profitability': self._get_profitability_metrics(),
                'growth': self._get_growth_metrics(),
                'financial_health': self._get_financial_health_metrics(),
                'dividends': self._get_dividend_metrics(),
                'other': self._get_other_metrics(),
            }
            
            return fundamentals
            
        except Exception as e:
            print(f"Error fetching fundamentals for {self.ticker}: {e}")
            return self._empty_fundamentals()
    
    def _get_valuation_metrics(self) -> Dict[str, Any]:
        """Extract valuation metrics."""
        return {
            'pe_trailing': self._safe_get('trailingPE'),
            'pe_forward': self._safe_get('forwardPE'),
            'pb_ratio': self._safe_get('priceToBook'),
            'peg_ratio': self._safe_get('pegRatio'),
            'market_cap': self._safe_get('marketCap'),
            'enterprise_value': self._safe_get('enterpriseValue'),
            'price_to_sales': self._safe_get('priceToSalesTrailing12Months'),
        }
    
    def _get_profitability_metrics(self) -> Dict[str, Any]:
        """Extract profitability metrics."""
        return {
            'profit_margin': self._safe_get('profitMargins'),
            'operating_margin': self._safe_get('operatingMargins'),
            'roe': self._safe_get('returnOnEquity'),
            'roa': self._safe_get('returnOnAssets'),
            'gross_margin': self._safe_get('grossMargins'),
            'ebitda_margin': self._safe_get('ebitdaMargins'),
        }
    
    def _get_growth_metrics(self) -> Dict[str, Any]:
        """Extract growth metrics."""
        return {
            'revenue_growth': self._safe_get('revenueGrowth'),
            'earnings_growth': self._safe_get('earningsGrowth'),
            'eps': self._safe_get('trailingEps'),
            'eps_forward': self._safe_get('forwardEps'),
            'revenue_per_share': self._safe_get('revenuePerShare'),
            'earnings_quarterly_growth': self._safe_get('earningsQuarterlyGrowth'),
        }
    
    def _get_financial_health_metrics(self) -> Dict[str, Any]:
        """Extract financial health metrics."""
        return {
            'debt_to_equity': self._safe_get('debtToEquity'),
            'current_ratio': self._safe_get('currentRatio'),
            'quick_ratio': self._safe_get('quickRatio'),
            'free_cash_flow': self._safe_get('freeCashflow'),
            'operating_cash_flow': self._safe_get('operatingCashflow'),
            'total_cash': self._safe_get('totalCash'),
            'total_debt': self._safe_get('totalDebt'),
        }
    
    def _get_dividend_metrics(self) -> Dict[str, Any]:
        """Extract dividend metrics."""
        dividend_yield = self._safe_get('dividendYield')
        payout_ratio = self._safe_get('payoutRatio')
        ex_dividend_date = self._safe_get('exDividendDate')
        
        # Validate dividend yield (sometimes yfinance returns bad data)
        if dividend_yield is not None and (dividend_yield > 1.0 or dividend_yield < 0):
            dividend_yield = None
        
        # Validate payout ratio
        if payout_ratio is not None and (payout_ratio > 10.0 or payout_ratio < -1.0):
            payout_ratio = None
        
        # Convert timestamp to readable date
        if ex_dividend_date:
            try:
                ex_dividend_date = datetime.fromtimestamp(ex_dividend_date).strftime('%Y-%m-%d')
            except:
                ex_dividend_date = None
        
        return {
            'dividend_yield': dividend_yield,
            'payout_ratio': payout_ratio,
            'ex_dividend_date': ex_dividend_date,
            'dividend_rate': self._safe_get('dividendRate'),
            'five_year_avg_dividend_yield': self._safe_get('fiveYearAvgDividendYield'),
        }
    
    def _get_other_metrics(self) -> Dict[str, Any]:
        """Extract other important metrics."""
        earnings_date = self._safe_get('earningsDate')
        if earnings_date and isinstance(earnings_date, (list, tuple)) and len(earnings_date) > 0:
            try:
                earnings_date = datetime.fromtimestamp(earnings_date[0]).strftime('%Y-%m-%d')
            except:
                earnings_date = None
        
        return {
            'beta': self._safe_get('beta'),
            'fifty_two_week_high': self._safe_get('fiftyTwoWeekHigh'),
            'fifty_two_week_low': self._safe_get('fiftyTwoWeekLow'),
            'fifty_day_average': self._safe_get('fiftyDayAverage'),
            'two_hundred_day_average': self._safe_get('twoHundredDayAverage'),
            'earnings_date': earnings_date,
            'shares_outstanding': self._safe_get('sharesOutstanding'),
        }
    
    def _safe_get(self, key: str) -> Optional[Any]:
        """Safely get value from info dict."""
        if self.info is None:
            return None
        return self.info.get(key, None)
    
    def _empty_fundamentals(self) -> Dict[str, Any]:
        """Return empty fundamentals structure."""
        return {
            'valuation': {},
            'profitability': {},
            'growth': {},
            'financial_health': {},
            'dividends': {},
            'other': {},
        }
    
    def calculate_health_score(self, fundamentals: Dict[str, Any]) -> Tuple[int, Dict[str, Any]]:
        """
        Calculate overall investment health score (0-100) and analysis.
        
        Args:
            fundamentals: Dictionary with fundamental metrics
            
        Returns:
            Tuple of (score, analysis_dict)
        """
        score = 0
        max_score = 0
        red_flags = []
        strengths = []
        
        val = fundamentals['valuation']
        prof = fundamentals['profitability']
        growth = fundamentals['growth']
        health = fundamentals['financial_health']
        div = fundamentals['dividends']
        other = fundamentals['other']
        
        # Valuation Score (20 points)
        if val.get('pe_trailing'):
            max_score += 10
            if 10 < val['pe_trailing'] < 25:
                score += 10
                strengths.append("Healthy P/E ratio (10-25)")
            elif val['pe_trailing'] > 40:
                score += 2
                red_flags.append(f"High P/E ratio ({val['pe_trailing']:.1f}) - may be overvalued")
            elif val['pe_trailing'] > 0:
                score += 6
        
        if val.get('peg_ratio'):
            max_score += 10
            if 0 < val['peg_ratio'] < 1:
                score += 10
                strengths.append(f"Excellent PEG ratio ({val['peg_ratio']:.2f}) - undervalued growth")
            elif 1 <= val['peg_ratio'] < 2:
                score += 7
                strengths.append("Good PEG ratio (1-2)")
            elif val['peg_ratio'] > 3:
                red_flags.append(f"High PEG ratio ({val['peg_ratio']:.2f})")
                score += 2
        
        # Profitability Score (25 points)
        if prof.get('profit_margin'):
            max_score += 8
            if prof['profit_margin'] > 0.20:
                score += 8
                strengths.append(f"Strong profit margin ({prof['profit_margin']*100:.1f}%)")
            elif prof['profit_margin'] > 0.10:
                score += 6
            elif prof['profit_margin'] < 0:
                red_flags.append(f"Negative profit margin ({prof['profit_margin']*100:.1f}%)")
        
        if prof.get('roe'):
            max_score += 9
            if prof['roe'] > 0.15:
                score += 9
                strengths.append(f"Excellent ROE ({prof['roe']*100:.1f}%)")
            elif prof['roe'] > 0.10:
                score += 6
            elif prof['roe'] < 0:
                red_flags.append(f"Negative ROE ({prof['roe']*100:.1f}%)")
        
        if prof.get('operating_margin'):
            max_score += 8
            if prof['operating_margin'] > 0.15:
                score += 8
            elif prof['operating_margin'] > 0.05:
                score += 5
            elif prof['operating_margin'] < 0:
                red_flags.append("Negative operating margin")
        
        # Growth Score (20 points)
        if growth.get('revenue_growth'):
            max_score += 10
            if growth['revenue_growth'] > 0.15:
                score += 10
                strengths.append(f"Strong revenue growth ({growth['revenue_growth']*100:.1f}%)")
            elif growth['revenue_growth'] > 0.05:
                score += 7
            elif growth['revenue_growth'] < 0:
                red_flags.append(f"Negative revenue growth ({growth['revenue_growth']*100:.1f}%)")
        
        if growth.get('earnings_growth'):
            max_score += 10
            if growth['earnings_growth'] > 0.15:
                score += 10
                strengths.append(f"Strong earnings growth ({growth['earnings_growth']*100:.1f}%)")
            elif growth['earnings_growth'] > 0.05:
                score += 7
            elif growth['earnings_growth'] < 0:
                red_flags.append(f"Negative earnings growth ({growth['earnings_growth']*100:.1f}%)")
        
        # Financial Health Score (25 points)
        if health.get('debt_to_equity') is not None:
            max_score += 10
            if health['debt_to_equity'] < 50:
                score += 10
                strengths.append(f"Low debt-to-equity ({health['debt_to_equity']:.1f})")
            elif health['debt_to_equity'] < 100:
                score += 7
            elif health['debt_to_equity'] > 200:
                score += 2
                red_flags.append(f"High debt-to-equity ratio ({health['debt_to_equity']:.1f})")
        
        if health.get('current_ratio'):
            max_score += 8
            if health['current_ratio'] > 2.0:
                score += 8
                strengths.append(f"Excellent current ratio ({health['current_ratio']:.2f})")
            elif health['current_ratio'] > 1.5:
                score += 6
            elif health['current_ratio'] < 1.0:
                red_flags.append(f"Low current ratio ({health['current_ratio']:.2f}) - liquidity concerns")
                score += 2
        
        if health.get('free_cash_flow'):
            max_score += 7
            if health['free_cash_flow'] > 0:
                score += 7
                if health['free_cash_flow'] > 1e9:  # > $1B
                    strengths.append("Strong free cash flow")
            else:
                red_flags.append("Negative free cash flow")
        
        # Dividend Score (10 points) - bonus for dividend payers
        if div.get('dividend_yield') and div['dividend_yield'] > 0:
            max_score += 5
            if 0.02 < div['dividend_yield'] < 0.06:
                score += 5
                strengths.append(f"Healthy dividend yield ({div['dividend_yield']*100:.1f}%)")
            elif div['dividend_yield'] > 0.08:
                red_flags.append(f"Very high dividend yield ({div['dividend_yield']*100:.1f}%) - sustainability risk")
                score += 2
        
            if div.get('payout_ratio'):
                max_score += 5
                if 0 < div['payout_ratio'] < 0.6:
                    score += 5
                    strengths.append("Sustainable payout ratio")
                elif div['payout_ratio'] > 0.8:
                    red_flags.append(f"High payout ratio ({div['payout_ratio']*100:.0f}%) - sustainability risk")
        
        # Calculate final score (0-100)
        if max_score > 0:
            final_score = int((score / max_score) * 100)
        else:
            final_score = 0
        
        # Determine valuation status
        valuation_status = self._determine_valuation(fundamentals)
        
        analysis = {
            'score': final_score,
            'red_flags': red_flags,
            'strengths': strengths,
            'valuation_status': valuation_status,
            'max_score': max_score,
            'earned_score': score,
        }
        
        return final_score, analysis
    
    def _determine_valuation(self, fundamentals: Dict[str, Any]) -> str:
        """
        Determine if stock is undervalued, fairly valued, or overvalued.
        
        Args:
            fundamentals: Dictionary with fundamental metrics
            
        Returns:
            Valuation status string
        """
        signals = []
        
        val = fundamentals['valuation']
        
        # P/E ratio analysis
        if val.get('pe_trailing'):
            if val['pe_trailing'] < 15:
                signals.append('undervalued')
            elif val['pe_trailing'] > 30:
                signals.append('overvalued')
            else:
                signals.append('fair')
        
        # PEG ratio analysis (most important)
        if val.get('peg_ratio'):
            if val['peg_ratio'] < 1:
                signals.append('undervalued')
                signals.append('undervalued')  # Weight this more
            elif val['peg_ratio'] > 2:
                signals.append('overvalued')
                signals.append('overvalued')
            else:
                signals.append('fair')
        
        # P/B ratio analysis
        if val.get('pb_ratio'):
            if val['pb_ratio'] < 1.5:
                signals.append('undervalued')
            elif val['pb_ratio'] > 5:
                signals.append('overvalued')
            else:
                signals.append('fair')
        
        # Count signals
        if not signals:
            return "Insufficient data"
        
        undervalued_count = signals.count('undervalued')
        overvalued_count = signals.count('overvalued')
        fair_count = signals.count('fair')
        
        if undervalued_count > overvalued_count and undervalued_count > fair_count:
            return "Undervalued ✅"
        elif overvalued_count > undervalued_count and overvalued_count > fair_count:
            return "Overvalued ⚠️"
        else:
            return "Fairly Valued ⚖️"
    
    def get_metric_interpretation(self, metric_name: str, value: Any) -> str:
        """
        Get human-readable interpretation of a metric.
        
        Args:
            metric_name: Name of the metric
            value: Value of the metric
            
        Returns:
            Interpretation string
        """
        if value is None:
            return "Data not available"
        
        interpretations = {
            'pe_trailing': self._interpret_pe_ratio,
            'pe_forward': self._interpret_pe_ratio,
            'pb_ratio': self._interpret_pb_ratio,
            'peg_ratio': self._interpret_peg_ratio,
            'profit_margin': self._interpret_profit_margin,
            'roe': self._interpret_roe,
            'debt_to_equity': self._interpret_debt_to_equity,
            'current_ratio': self._interpret_current_ratio,
            'dividend_yield': self._interpret_dividend_yield,
            'beta': self._interpret_beta,
        }
        
        interpreter = interpretations.get(metric_name)
        if interpreter:
            return interpreter(value)
        
        return ""
    
    def _interpret_pe_ratio(self, value: float) -> str:
        """Interpret P/E ratio."""
        if value < 0:
            return "⚠️ Negative (company is losing money)"
        elif value < 15:
            return "✅ Low - potentially undervalued"
        elif value < 25:
            return "✅ Moderate - healthy valuation"
        elif value < 40:
            return "⚠️ High - may be overvalued"
        else:
            return "🔴 Very high - expensive relative to earnings"
    
    def _interpret_pb_ratio(self, value: float) -> str:
        """Interpret P/B ratio."""
        if value < 1:
            return "✅ Below book value - potentially undervalued"
        elif value < 3:
            return "✅ Reasonable - trading near book value"
        elif value < 5:
            return "⚠️ Above book value - justified if high growth"
        else:
            return "⚠️ High - expensive relative to assets"
    
    def _interpret_peg_ratio(self, value: float) -> str:
        """Interpret PEG ratio."""
        if value < 0:
            return "⚠️ Negative growth expectations"
        elif value < 1:
            return "✅ Excellent - undervalued relative to growth"
        elif value < 1.5:
            return "✅ Good - fairly valued for growth"
        elif value < 2:
            return "⚖️ Fair - slight premium for growth"
        else:
            return "⚠️ High - expensive even with growth"
    
    def _interpret_profit_margin(self, value: float) -> str:
        """Interpret profit margin."""
        value_pct = value * 100
        if value_pct < 0:
            return "🔴 Negative - company is losing money"
        elif value_pct < 5:
            return "⚠️ Low - thin margins"
        elif value_pct < 10:
            return "⚖️ Moderate - acceptable margins"
        elif value_pct < 20:
            return "✅ Good - healthy profitability"
        else:
            return "✅ Excellent - very profitable"
    
    def _interpret_roe(self, value: float) -> str:
        """Interpret ROE."""
        value_pct = value * 100
        if value_pct < 0:
            return "🔴 Negative - destroying shareholder value"
        elif value_pct < 10:
            return "⚠️ Low - poor returns on equity"
        elif value_pct < 15:
            return "⚖️ Moderate - acceptable returns"
        elif value_pct < 20:
            return "✅ Good - strong returns on equity"
        else:
            return "✅ Excellent - exceptional returns"
    
    def _interpret_debt_to_equity(self, value: float) -> str:
        """Interpret debt-to-equity ratio."""
        if value < 30:
            return "✅ Very low - minimal debt"
        elif value < 50:
            return "✅ Low - conservative leverage"
        elif value < 100:
            return "⚖️ Moderate - balanced leverage"
        elif value < 200:
            return "⚠️ High - substantial debt burden"
        else:
            return "🔴 Very high - risky debt levels"
    
    def _interpret_current_ratio(self, value: float) -> str:
        """Interpret current ratio."""
        if value < 1:
            return "🔴 Poor - may struggle to meet short-term obligations"
        elif value < 1.5:
            return "⚠️ Low - limited liquidity buffer"
        elif value < 2:
            return "✅ Good - adequate liquidity"
        elif value < 3:
            return "✅ Strong - excellent liquidity"
        else:
            return "⚖️ Very high - may be inefficient with assets"
    
    def _interpret_dividend_yield(self, value: float) -> str:
        """Interpret dividend yield."""
        value_pct = value * 100
        if value_pct == 0:
            return "No dividend - growth-focused company"
        elif value_pct < 2:
            return "✅ Low - company prioritizing growth"
        elif value_pct < 4:
            return "✅ Moderate - balanced approach"
        elif value_pct < 6:
            return "✅ High - strong income potential"
        else:
            return "⚠️ Very high - verify sustainability"
    
    def _interpret_beta(self, value: float) -> str:
        """Interpret beta."""
        if value < 0:
            return "⚖️ Negative correlation with market"
        elif value < 0.5:
            return "✅ Very low volatility - defensive stock"
        elif value < 1:
            return "✅ Low volatility - less risky than market"
        elif value < 1.5:
            return "⚖️ Moderate volatility - slightly more volatile than market"
        elif value < 2:
            return "⚠️ High volatility - significantly more risky"
        else:
            return "🔴 Very high volatility - extremely risky"
