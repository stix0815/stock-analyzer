# Stock Analysis Bot - Probabilistic Trading Algorithm

A comprehensive stock analysis system that combines technical indicators, probabilistic models, SEC filings, sentiment analysis, and real-time metrics to provide bullish/bearish recommendations.

## Architecture

```
stock_analyzer/
├── data_sources/          # Data collection modules
│   ├── price_data.py      # Historical/real-time price data
│   ├── sec_filings.py     # SEC EDGAR API integration
│   ├── news_sentiment.py  # News & social media sentiment
│   ├── order_book.py      # Order book dynamics
│   └── market_data.py     # VIX, volatility, market-wide metrics
├── indicators/            # Technical indicator calculations
│   ├── trend.py          # MACD, SMA, EMA
│   ├── momentum.py       # RSI, Stochastic
│   ├── volatility.py     # Bollinger Bands, ATR
│   └── volume.py         # Volume profiles, OBV
├── models/               # Probabilistic & ML models
│   ├── monte_carlo.py    # Monte Carlo simulations
│   ├── bayesian.py       # Bayesian inference
│   ├── mean_reversion.py # Statistical arbitrage
│   └── pattern_detect.py # Pattern recognition
├── analysis/             # Analysis engines
│   ├── technical.py      # Technical analysis scoring
│   ├── fundamental.py    # SEC filing analysis
│   ├── sentiment.py      # Sentiment scoring
│   └── probability.py    # Probabilistic forecasting
├── core/                 # Core orchestration
│   ├── analyzer.py       # Main analysis engine
│   ├── scorer.py         # Bull/bear scoring system
│   └── reporter.py       # Report generation
├── config.py             # Configuration
├── requirements.txt      # Dependencies
└── main.py              # Entry point
```

## Features

### Technical Indicators
- **Trend**: MACD, SMA (50/200), EMA, Golden/Death Cross
- **Momentum**: RSI, Stochastic Oscillator
- **Volatility**: Bollinger Bands, ATR, Band Squeeze
- **Volume**: Volume profiles, OBV, liquidity analysis

### Probabilistic Models
- Monte Carlo price path simulations
- Bayesian probability updates
- Mean reversion detection
- Statistical arbitrage signals

### Real-Time Metrics
- Order book imbalances
- Bid-ask spreads
- VIX correlation analysis
- Tick Index sentiment
- Liquidity patterns

### Fundamental Analysis
- SEC 13D/13F filings
- Earnings sentiment (NLP on transcripts)
- Insider trading patterns
- News event catalysts

### Market Behavior
- Flash crash patterns
- Circuit breaker probabilities
- Retail FOMO metrics
- Mean reversion timing

## Usage

```python
from stock_analyzer import StockAnalyzer

analyzer = StockAnalyzer()
result = analyzer.analyze('AAPL')

print(result.bullish_score)  # 0-100
print(result.bearish_score)  # 0-100
print(result.recommendation)  # BUY/SELL/HOLD
print(result.confidence)      # 0-100
print(result.scenarios)       # Detailed bull/bear scenarios
```

## Installation

```bash
pip install -r requirements.txt
```

## API Keys Required

- Alpha Vantage (free tier available)
- SEC EDGAR (no key required)
- News API / Financial Modeling Prep
- Optional: Twitter API for sentiment
