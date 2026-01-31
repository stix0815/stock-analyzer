# Stock Analysis Streamlit App

A professional stock analysis tool built with Streamlit that provides technical analysis, BUY/SELL/HOLD recommendations, and Monte Carlo simulations.

## 🎯 Features

- **Technical Indicators**
  - RSI (Relative Strength Index)
  - MACD (Moving Average Convergence Divergence)
  - Bollinger Bands
  - SMA (50-day and 200-day)
  - Volume Analysis

- **Smart Scoring System**
  - Timeframe-dependent weighting
  - Risk tolerance adjustments
  - Confidence levels

- **Scenario Analysis**
  - Bull case with probability
  - Bear case with probability
  - Monte Carlo simulation (1000 iterations)

- **Interactive Visualizations**
  - Candlestick charts
  - Technical indicator overlays
  - Monte Carlo simulation paths

- **Professional UI/UX**
  - Clean, modern interface
  - Disclaimer and risk acceptance
  - Responsive design
  - Real-time analysis

## 🚀 Quick Start

### Installation

1. **Clone or navigate to the app directory:**
   ```bash
   cd stock_analyzer/streamlit_app
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app:**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser:**
   The app will automatically open at `http://localhost:8501`

## 📋 Usage

1. **Accept Disclaimer**
   - First-time users must accept the educational use disclaimer

2. **Enter Analysis Parameters**
   - **Stock Ticker:** Enter symbol (e.g., AAPL, TSLA, NVDA)
   - **Timeframe:** Choose Short/Medium/Long term
   - **Risk Tolerance:** Select Conservative/Moderate/Aggressive

3. **Analyze**
   - Click "Analyze Stock" button
   - View comprehensive analysis results

4. **Interpret Results**
   - **Summary View:** Quick BUY/SELL/HOLD signal with score
   - **Bull/Bear Scenarios:** Probabilistic outcomes
   - **Charts:** Interactive price and indicator visualizations
   - **Detailed Analysis:** Full breakdown of all indicators

## 📊 Analysis Components

### Summary View
- Current signal (BUY/SELL/HOLD)
- Overall score (0-100)
- Confidence level
- Bull and bear case probabilities

### Detailed Analysis
- Individual indicator scores
- Signal interpretations
- Supporting evidence
- Risk/reward ratios

### Charts
- **Price Chart:** Candlesticks with Bollinger Bands and SMAs
- **MACD Chart:** MACD line, signal line, and histogram
- **RSI Chart:** With overbought/oversold levels
- **Volume Chart:** Color-coded by price movement
- **Monte Carlo:** Simulation paths and distribution

## 🎲 Timeframes

### Short-term (1-7 days)
- Focus on RSI and MACD
- Higher weight on momentum indicators
- Quick entry/exit recommendations

### Medium-term (1-4 weeks)
- Balanced indicator weighting
- Trend confirmation important
- Standard position sizing

### Long-term (1-6 months)
- Emphasis on SMAs and fundamentals
- P/E ratio and profit margins considered
- Lower frequency trading

## 🎯 Risk Tolerance

### Conservative
- Only high-confidence signals (>75% score)
- Smaller position sizes (2-3%)
- Tighter stop-losses
- Emphasize risk factors

### Moderate (Default)
- Balanced approach (>60% score)
- Standard position sizes (3-5%)
- Normal stop-losses
- Risk/reward balanced

### Aggressive
- Accept lower confidence (>50% score)
- Larger position sizes (7-10%)
- Wider stop-losses
- Emphasize upside potential

## 🛠️ Technical Stack

- **Frontend:** Streamlit
- **Data:** yfinance (Yahoo Finance API)
- **Calculations:** pandas, numpy
- **Charts:** Plotly
- **Simulations:** scipy, numpy

## 📁 File Structure

```
streamlit_app/
├── app.py                 # Main Streamlit application
├── data_fetcher.py        # yfinance data fetching
├── indicators.py          # Technical indicator calculations
├── scoring.py             # Scoring system logic
├── monte_carlo.py         # Monte Carlo simulation
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## ⚠️ Disclaimer

**IMPORTANT:** This tool is for **educational purposes only**.

- ❌ NOT financial advice
- ❌ NOT investment recommendations
- ❌ NO guarantee of future performance

**Always:**
- ✅ Do your own research
- ✅ Consult a licensed financial advisor
- ✅ Understand that trading involves risk of loss

**The creators are NOT liable for any financial losses incurred from using this tool.**

## 🧪 Testing

Test the app with these tickers:
- **AAPL** - Large cap tech
- **TSLA** - High volatility
- **NVDA** - Growth stock

Try different timeframes and risk tolerances to see how recommendations change.

## 🚀 Deployment

### Streamlit Cloud (Recommended)

1. Push code to GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Deploy the `app.py` file
5. Your app will be live at a public URL!

### Local Deployment

```bash
streamlit run app.py --server.port 8501
```

## 📈 Future Enhancements

Potential additions:
- News sentiment analysis
- SEC filing integration
- Options strategy suggestions
- Portfolio backtesting
- Email alerts
- Multi-stock comparison

## 🤝 Contributing

This is an educational project. Feel free to fork and modify for your own learning!

## 📄 License

Educational use only. See disclaimer above.

## 📧 Support

For issues or questions, please refer to the Streamlit documentation or yfinance documentation.

---

**Built with ❤️ for educational purposes**
