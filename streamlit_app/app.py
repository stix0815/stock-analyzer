"""
Streamlit Stock Analysis App
Educational stock analysis tool with technical indicators and Monte Carlo simulation.
"""
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime

from data_fetcher import DataFetcher
from indicators import TechnicalIndicators
from scoring import ScoringSystem
from monte_carlo import MonteCarloSimulator


# Page configuration
st.set_page_config(
    page_title="Stock Analysis Tool",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 2px solid #ffc107;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .signal-buy {
        color: #28a745;
        font-weight: bold;
        font-size: 1.5rem;
    }
    .signal-sell {
        color: #dc3545;
        font-weight: bold;
        font-size: 1.5rem;
    }
    .signal-hold {
        color: #ffc107;
        font-weight: bold;
        font-size: 1.5rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 5px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)


def show_disclaimer():
    """Display disclaimer and risk acceptance."""
    if 'disclaimer_accepted' not in st.session_state:
        st.session_state.disclaimer_accepted = False
    
    if not st.session_state.disclaimer_accepted:
        st.markdown('<div class="main-header">⚠️ IMPORTANT DISCLAIMER</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="warning-box">
        <h3>📋 Educational Use Only</h3>
        
        This tool provides **EDUCATIONAL analysis only**.
        
        **❌ This is NOT:**
        - Financial advice
        - Investment recommendations
        - A guarantee of future performance
        
        **✅ You should:**
        - Always do your own research
        - Consult a licensed financial advisor
        - Understand that trading involves significant risk of loss
        
        **⚠️ Important Notes:**
        - Past performance does NOT guarantee future results
        - You could lose all invested capital
        - The creators are NOT liable for any losses
        
        **By continuing, you acknowledge:**
        - ☐ This is for educational purposes only
        - ☐ I understand the risk of financial loss
        - ☐ I will not hold creators liable for losses
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("✅ I Understand & Accept", type="primary", use_container_width=True):
                st.session_state.disclaimer_accepted = True
                st.rerun()
        
        st.stop()


def get_timeframe_days(timeframe: str) -> int:
    """Get number of days for Monte Carlo simulation based on timeframe."""
    timeframe_map = {
        "Short-term (1-7 days)": 7,
        "Medium-term (1-4 weeks)": 28,
        "Long-term (1-6 months)": 180
    }
    return timeframe_map.get(timeframe, 7)


def create_price_chart(data: pd.DataFrame, indicators: dict, stock_name: str):
    """Create interactive price chart with indicators."""
    fig = make_subplots(
        rows=4, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        subplot_titles=(f'{stock_name} Price & Bollinger Bands', 'MACD', 'RSI', 'Volume'),
        row_heights=[0.5, 0.15, 0.15, 0.2]
    )
    
    # Price and Bollinger Bands
    fig.add_trace(
        go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name='Price'
        ),
        row=1, col=1
    )
    
    if 'bollinger' in indicators:
        bb = indicators['bollinger']
        fig.add_trace(
            go.Scatter(x=data.index, y=bb['upper_series'], name='BB Upper',
                      line=dict(color='gray', dash='dash')),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(x=data.index, y=bb['middle_series'], name='BB Middle',
                      line=dict(color='orange')),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(x=data.index, y=bb['lower_series'], name='BB Lower',
                      line=dict(color='gray', dash='dash')),
            row=1, col=1
        )
    
    # SMAs
    if 'sma' in indicators:
        sma = indicators['sma']
        if sma['sma_50'] is not None:
            fig.add_trace(
                go.Scatter(x=data.index, y=sma['sma_50_series'], name='SMA 50',
                          line=dict(color='blue')),
                row=1, col=1
            )
        if sma['sma_200'] is not None:
            fig.add_trace(
                go.Scatter(x=data.index, y=sma['sma_200_series'], name='SMA 200',
                          line=dict(color='red')),
                row=1, col=1
            )
    
    # MACD
    if 'macd' in indicators:
        macd = indicators['macd']
        fig.add_trace(
            go.Scatter(x=data.index, y=macd['macd_series'], name='MACD',
                      line=dict(color='blue')),
            row=2, col=1
        )
        fig.add_trace(
            go.Scatter(x=data.index, y=macd['signal_series'], name='Signal',
                      line=dict(color='red')),
            row=2, col=1
        )
        fig.add_trace(
            go.Bar(x=data.index, y=macd['histogram_series'], name='Histogram',
                  marker_color='gray'),
            row=2, col=1
        )
    
    # RSI
    if 'rsi' in indicators:
        rsi = indicators['rsi']
        fig.add_trace(
            go.Scatter(x=data.index, y=rsi['series'], name='RSI',
                      line=dict(color='purple')),
            row=3, col=1
        )
        fig.add_hline(y=70, line_dash="dash", line_color="red", row=3, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="green", row=3, col=1)
    
    # Volume
    if 'volume' in indicators:
        colors = ['red' if data['Close'].iloc[i] < data['Open'].iloc[i] else 'green' 
                 for i in range(len(data))]
        fig.add_trace(
            go.Bar(x=data.index, y=data['Volume'], name='Volume',
                  marker_color=colors),
            row=4, col=1
        )
    
    fig.update_layout(
        height=1000,
        showlegend=True,
        xaxis_rangeslider_visible=False,
        hovermode='x unified'
    )
    
    fig.update_xaxes(title_text="Date", row=4, col=1)
    fig.update_yaxes(title_text="Price ($)", row=1, col=1)
    fig.update_yaxes(title_text="MACD", row=2, col=1)
    fig.update_yaxes(title_text="RSI", row=3, col=1)
    fig.update_yaxes(title_text="Volume", row=4, col=1)
    
    return fig


def create_monte_carlo_chart(simulation_results: dict):
    """Create Monte Carlo simulation visualization."""
    simulations = simulation_results['simulations']
    days = simulation_results['days']
    current_price = simulation_results['current_price']
    
    fig = go.Figure()
    
    # Plot subset of simulations (for performance)
    sample_size = min(100, len(simulations))
    indices = np.random.choice(len(simulations), sample_size, replace=False)
    
    for idx in indices:
        fig.add_trace(
            go.Scatter(
                x=list(range(days)),
                y=simulations[idx],
                mode='lines',
                line=dict(color='lightblue', width=0.5),
                showlegend=False,
                opacity=0.3
            )
        )
    
    # Add median line
    median_path = np.median(simulations, axis=0)
    fig.add_trace(
        go.Scatter(
            x=list(range(days)),
            y=median_path,
            mode='lines',
            name='Median',
            line=dict(color='blue', width=3)
        )
    )
    
    # Add starting price
    fig.add_hline(y=current_price, line_dash="dash", line_color="black",
                  annotation_text=f"Current: ${current_price:.2f}")
    
    fig.update_layout(
        title="Monte Carlo Simulation (1000 iterations)",
        xaxis_title="Days",
        yaxis_title="Price ($)",
        height=500,
        hovermode='x unified'
    )
    
    return fig


def display_summary(stock_info: dict, score_results: dict, scenarios: dict, timeframe: str):
    """Display summary view."""
    st.markdown("---")
    st.markdown('<div class="main-header">📊 ANALYSIS SUMMARY</div>', unsafe_allow_html=True)
    
    # Header with stock info
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"### {stock_info['name']} ({stock_info.get('ticker', '')})")
    with col2:
        price_change = ((stock_info['current_price'] - stock_info['previous_close']) / 
                       stock_info['previous_close'] * 100)
        st.metric(
            "Current Price",
            f"${stock_info['current_price']:.2f}",
            f"{price_change:+.2f}%"
        )
    
    # Signal and score
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        signal = score_results['signal']
        signal_class = "signal-buy" if "BUY" in signal else "signal-sell" if "SELL" in signal else "signal-hold"
        st.markdown(f'<div class="{signal_class}">🎯 {signal}</div>', unsafe_allow_html=True)
    
    with col2:
        st.metric("Score", f"{score_results['score']}/100")
    
    with col3:
        st.metric("Confidence", score_results['confidence'])
    
    st.markdown(f"**Timeframe:** {timeframe}")
    st.markdown(f"**Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}")
    
    # Bull and Bear scenarios
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🟢 BULL CASE")
        bull = scenarios['bull']
        st.markdown(f"**Probability:** {bull['probability']:.1f}%")
        st.markdown(bull['description'])
    
    with col2:
        st.markdown("### 🔴 BEAR CASE")
        bear = scenarios['bear']
        st.markdown(f"**Probability:** {bear['probability']:.1f}%")
        st.markdown(bear['description'])


def display_detailed_analysis(indicators: dict, score_results: dict, stock_info: dict):
    """Display detailed technical analysis."""
    st.markdown("---")
    st.markdown("## 📈 DETAILED TECHNICAL ANALYSIS")
    
    with st.expander("📊 Technical Indicators Breakdown", expanded=True):
        # RSI
        if 'rsi' in indicators:
            st.markdown("### RSI (Relative Strength Index)")
            rsi = indicators['rsi']
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("RSI Value", f"{rsi['value']:.1f}")
            with col2:
                st.metric("Signal", rsi['signal'])
            with col3:
                if 'rsi' in score_results['breakdown']:
                    st.metric("Score", f"{score_results['breakdown']['rsi']['weighted']:.0f}/{score_results['breakdown']['rsi']['max']}")
            
            # Interpretation
            if rsi['value'] < 30:
                st.info("💡 **Oversold** - Price may rebound. Historical rebounds from RSI<30 are common.")
            elif rsi['value'] > 70:
                st.warning("💡 **Overbought** - Price may pull back. Consider waiting for better entry.")
            
            st.markdown("---")
        
        # MACD
        if 'macd' in indicators:
            st.markdown("### MACD (Moving Average Convergence Divergence)")
            macd = indicators['macd']
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("MACD Line", f"{macd['macd_line']:.2f}")
            with col2:
                st.metric("Signal Line", f"{macd['signal_line']:.2f}")
            with col3:
                st.metric("Histogram", f"{macd['histogram']:.2f}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Signal", macd['signal'])
            with col2:
                if 'macd' in score_results['breakdown']:
                    st.metric("Score", f"{score_results['breakdown']['macd']['weighted']:.0f}/{score_results['breakdown']['macd']['max']}")
            
            if macd['signal'] == "BULLISH":
                st.success("💡 MACD crossed above signal line - Momentum building upward.")
            elif macd['signal'] == "BEARISH":
                st.error("💡 MACD crossed below signal line - Momentum turning downward.")
            
            st.markdown("---")
        
        # Bollinger Bands
        if 'bollinger' in indicators:
            st.markdown("### Bollinger Bands")
            bb = indicators['bollinger']
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Upper Band", f"${bb['upper']:.2f}")
            with col2:
                st.metric("Middle (SMA)", f"${bb['middle']:.2f}")
            with col3:
                st.metric("Lower Band", f"${bb['lower']:.2f}")
            with col4:
                st.metric("Current", f"${bb['current']:.2f}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Signal", bb['signal'])
            with col2:
                if 'bollinger' in score_results['breakdown']:
                    st.metric("Score", f"{score_results['breakdown']['bollinger']['weighted']:.0f}/{score_results['breakdown']['bollinger']['max']}")
            
            st.markdown("---")
        
        # SMA
        if 'sma' in indicators:
            st.markdown("### Simple Moving Averages")
            sma = indicators['sma']
            col1, col2, col3 = st.columns(3)
            with col1:
                if sma['sma_50']:
                    st.metric("SMA 50", f"${sma['sma_50']:.2f}")
            with col2:
                if sma['sma_200']:
                    st.metric("SMA 200", f"${sma['sma_200']:.2f}")
            with col3:
                st.metric("Current", f"${sma['current']:.2f}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Signal", sma['signal'])
            with col2:
                if 'sma' in score_results['breakdown']:
                    st.metric("Score", f"{score_results['breakdown']['sma']['weighted']:.0f}/{score_results['breakdown']['sma']['max']}")
            
            st.markdown("---")
        
        # Volume
        if 'volume' in indicators:
            st.markdown("### Volume Analysis")
            vol = indicators['volume']
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Current Volume", f"{vol['current']:,.0f}")
            with col2:
                st.metric("Average Volume", f"{vol['average']:,.0f}")
            with col3:
                st.metric("Change", f"{vol['change_pct']:+.1f}%")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Signal", vol['signal'])
            with col2:
                if 'volume' in score_results['breakdown']:
                    st.metric("Score", f"{score_results['breakdown']['volume']['weighted']:.0f}/{score_results['breakdown']['volume']['max']}")


def main():
    """Main application."""
    # Show disclaimer first
    show_disclaimer()
    
    # App header
    st.markdown('<div class="main-header">📊 Stock Analysis Tool</div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666;">Educational stock analysis with technical indicators and Monte Carlo simulation</p>', unsafe_allow_html=True)
    
    # Sidebar inputs
    st.sidebar.header("⚙️ Analysis Settings")
    
    ticker = st.sidebar.text_input("Stock Ticker", "AAPL", help="Enter stock symbol (e.g., AAPL, TSLA, NVDA)").upper()
    
    timeframe_options = ["Short-term (1-7 days)", "Medium-term (1-4 weeks)", "Long-term (1-6 months)"]
    timeframe_display = st.sidebar.selectbox("⏱️ Trading Timeframe", timeframe_options)
    timeframe = timeframe_display.split()[0].lower()  # Extract 'short', 'medium', or 'long'
    
    risk_options = ["Conservative", "Moderate", "Aggressive"]
    risk_tolerance = st.sidebar.selectbox("🎲 Risk Tolerance", risk_options).lower()
    
    analyze_button = st.sidebar.button("🔍 Analyze Stock", type="primary", use_container_width=True)
    
    # Warning footer
    st.sidebar.markdown("---")
    st.sidebar.warning("⚠️ **Educational use only**\n\nNot financial advice")
    
    # Main analysis
    if analyze_button:
        if not ticker:
            st.error("Please enter a stock ticker symbol.")
            return
        
        with st.spinner(f"Analyzing {ticker}..."):
            # Fetch data
            fetcher = DataFetcher(ticker)
            
            # Validate ticker
            if not fetcher.validate_ticker():
                st.error(f"❌ Invalid ticker symbol: {ticker}")
                st.info("Please check the ticker and try again.")
                return
            
            # Get stock info
            stock_info = fetcher.get_stock_info()
            stock_info['ticker'] = ticker
            
            # Fetch historical data
            data = fetcher.fetch_data(timeframe)
            
            if data is None or data.empty:
                st.error(f"❌ Could not fetch data for {ticker}")
                return
            
            # Calculate indicators
            indicator_calc = TechnicalIndicators(data)
            indicators = indicator_calc.calculate_all()
            
            # Calculate score
            scorer = ScoringSystem(timeframe, risk_tolerance)
            score_results = scorer.calculate_score(indicators, stock_info)
            
            # Run Monte Carlo simulation
            days = get_timeframe_days(timeframe_display)
            mc_sim = MonteCarloSimulator(data)
            simulation_results = mc_sim.run_simulation(days, stock_info['current_price'])
            scenarios = mc_sim.get_scenarios(simulation_results)
            
            # Display results
            display_summary(stock_info, score_results, scenarios, timeframe_display)
            
            # Recommendation
            st.markdown("---")
            st.markdown("## 💡 RECOMMENDATION")
            
            col1, col2 = st.columns([2, 1])
            with col1:
                signal = score_results['signal']
                
                if "BUY" in signal:
                    st.success(f"**Action:** {signal}")
                    st.write(f"**Entry Range:** ${stock_info['current_price'] * 0.99:.2f} - ${stock_info['current_price'] * 1.01:.2f}")
                    st.write(f"**Target:** ${scenarios['bull']['target']:.2f} ({scenarios['bull']['change_pct']:+.1f}%)")
                    st.write(f"**Stop-Loss:** ${stock_info['current_price'] * 0.97:.2f}")
                    
                    if risk_tolerance == "conservative":
                        st.write("**Position Size:** 2-3% of portfolio")
                    elif risk_tolerance == "aggressive":
                        st.write("**Position Size:** 7-10% of portfolio")
                    else:
                        st.write("**Position Size:** 3-5% of portfolio")
                    
                elif "SELL" in signal:
                    st.error(f"**Action:** {signal}")
                    st.write("Consider exiting position or avoiding entry at this time.")
                    
                else:  # HOLD
                    st.warning(f"**Action:** {signal}")
                    st.write("Wait for better entry opportunity or maintain current position.")
            
            with col2:
                risk_reward = abs(scenarios['bull']['change_pct'] / scenarios['bear']['change_pct']) if scenarios['bear']['change_pct'] != 0 else 0
                st.metric("Risk/Reward Ratio", f"1:{risk_reward:.1f}")
            
            # Charts
            st.markdown("---")
            st.markdown("## 📊 INTERACTIVE CHARTS")
            
            tab1, tab2 = st.tabs(["Price & Indicators", "Monte Carlo Simulation"])
            
            with tab1:
                price_chart = create_price_chart(data, indicators, stock_info['name'])
                st.plotly_chart(price_chart, use_container_width=True)
            
            with tab2:
                st.markdown("### 🎲 Monte Carlo Simulation Results")
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Median Price", f"${simulation_results['median_price']:.2f}")
                with col2:
                    st.metric("Mean Price", f"${simulation_results['mean_price']:.2f}")
                with col3:
                    st.metric("10th Percentile", f"${simulation_results['percentile_10']:.2f}")
                with col4:
                    st.metric("90th Percentile", f"${simulation_results['percentile_90']:.2f}")
                
                mc_chart = create_monte_carlo_chart(simulation_results)
                st.plotly_chart(mc_chart, use_container_width=True)
                
                st.info(f"""
                **Simulation Parameters:**
                - Iterations: 1,000
                - Timeframe: {days} days
                - Daily Drift: {simulation_results['drift']*100:.3f}%
                - Daily Volatility: {simulation_results['volatility']*100:.2f}%
                """)
            
            # Detailed analysis
            display_detailed_analysis(indicators, score_results, stock_info)
    
    else:
        # Initial state - show instructions
        st.info("""
        ### 👋 Welcome to the Stock Analysis Tool!
        
        **How to use:**
        1. Enter a stock ticker (e.g., AAPL, TSLA, NVDA)
        2. Select your trading timeframe
        3. Choose your risk tolerance
        4. Click "Analyze Stock"
        
        **What you'll get:**
        - Technical analysis with RSI, MACD, Bollinger Bands, SMA, and Volume
        - BUY/SELL/HOLD recommendation with confidence level
        - Bull and Bear scenarios with probabilities
        - Monte Carlo simulation (1000 iterations)
        - Interactive charts
        
        **Remember:** This is for educational purposes only. Always do your own research!
        """)


if __name__ == "__main__":
    main()
