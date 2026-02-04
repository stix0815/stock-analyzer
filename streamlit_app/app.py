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
        color: #000000;
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
    /* Remove box around info icon popover */
    button[kind="secondary"] {
        border: none !important;
        background: none !important;
        padding: 0 !important;
        box-shadow: none !important;
    }
    button[kind="secondary"]:hover {
        background: none !important;
        border: none !important;
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


def generate_signal_reasoning(score_results: dict, indicators: dict, stock_info: dict) -> str:
    """Generate detailed reasoning for the trading signal."""
    signal = score_results['signal']
    score = score_results['score']
    breakdown = score_results['breakdown']
    
    reasoning = f"### 🧠 Signal Reasoning\n\n"
    reasoning += f"**Overall Score: {score}/100** ({score_results['confidence']} confidence)\n\n"
    
    # Explain score calculation
    reasoning += "#### 📊 Score Breakdown\n\n"
    reasoning += "Each indicator contributes to the total score based on its importance for your selected timeframe:\n\n"
    
    for indicator_name, details in breakdown.items():
        weighted = details['weighted']
        max_score = details['max']
        percentage = (weighted / max_score * 100) if max_score > 0 else 0
        reasoning += f"**{indicator_name.upper()}:** {weighted:.0f}/{max_score} points ({percentage:.0f}% efficiency)\n"
    
    reasoning += f"\n**Total:** {score}/100\n\n"
    
    # Count bullish vs bearish signals
    bullish_count = 0
    bearish_count = 0
    neutral_count = 0
    
    for ind_name, ind_data in indicators.items():
        if 'signal' in ind_data:
            sig = ind_data['signal']
            if 'BULLISH' in sig or 'ABOVE' in sig or 'HIGH VOLUME' in sig:
                bullish_count += 1
            elif 'BEARISH' in sig or 'BELOW' in sig or 'LOW VOLUME' in sig:
                bearish_count += 1
            else:
                neutral_count += 1
    
    total_signals = bullish_count + bearish_count + neutral_count
    
    reasoning += "---\n\n"
    reasoning += f"#### 🎯 Why **{signal}**?\n\n"
    reasoning += f"**Market Consensus:** {bullish_count} bullish / {bearish_count} bearish / {neutral_count} neutral signals\n\n"
    
    if "BUY" in signal:
        reasoning += "**✅ Strong Buy Case:**\n\n"
        reasoning += f"The score of {score}/100 indicates a favorable risk/reward setup. Here's why:\n\n"
        
        # Detailed indicator explanations
        if 'rsi' in indicators:
            rsi_val = indicators['rsi']['value']
            if rsi_val < 40:
                reasoning += f"**RSI ({rsi_val:.1f}):** Oversold territory suggests the stock has been sold off aggressively and may be due for a bounce. Historically, RSI below 40 often precedes short-term recoveries.\n\n"
            elif rsi_val < 60:
                reasoning += f"**RSI ({rsi_val:.1f}):** In neutral zone with room to run higher. Not showing overbought conditions, which means momentum can continue building.\n\n"
        
        if 'macd' in indicators and indicators['macd']['signal'] == 'BULLISH':
            reasoning += f"**MACD:** Bullish crossover detected (histogram: {indicators['macd']['histogram']:.2f}). This signals that short-term momentum is accelerating above the longer-term trend. When MACD crosses above its signal line, it often precedes price increases.\n\n"
        
        if 'bollinger' in indicators:
            bb_sig = indicators['bollinger']['signal']
            if 'LOWER' in bb_sig:
                reasoning += f"**Bollinger Bands:** Price near lower band (${indicators['bollinger']['lower']:.2f}). Statistically, prices tend to revert to the middle band (${indicators['bollinger']['middle']:.2f}), suggesting potential upside of {((indicators['bollinger']['middle'] - stock_info['current_price']) / stock_info['current_price'] * 100):.1f}%.\n\n"
            elif 'ABOVE' in bb_sig:
                reasoning += f"**Bollinger Bands:** Price above middle band shows bullish momentum. Current trend is upward.\n\n"
        
        if 'volume' in indicators and 'HIGH' in indicators['volume']['signal']:
            reasoning += f"**Volume:** {indicators['volume']['change_pct']:+.1f}% above average. High volume confirms genuine buying interest and validates the move. This isn't a low-conviction rally.\n\n"
        
        reasoning += f"**📈 Bottom Line:** With {bullish_count}/{total_signals} indicators bullish and a score above threshold, the technical setup favors entry at current levels.\n"
        
    elif "SELL" in signal:
        reasoning += "**⚠️ Warning Signs:**\n\n"
        reasoning += f"The score of {score}/100 is below safe thresholds. Here's why this is risky:\n\n"
        
        if 'rsi' in indicators and indicators['rsi']['value'] > 70:
            reasoning += f"**RSI ({indicators['rsi']['value']:.1f}):** Severely overbought. When RSI exceeds 70, it indicates excessive buying that typically leads to pullbacks. The stock is statistically \"expensive\" at current levels.\n\n"
        
        if 'macd' in indicators and indicators['macd']['signal'] == 'BEARISH':
            reasoning += f"**MACD:** Bearish crossover (histogram: {indicators['macd']['histogram']:.2f}). Momentum has turned negative. Short-term trend is now weaker than long-term, signaling potential decline.\n\n"
        
        if 'sma' in indicators and 'BEARISH' in indicators['sma']['signal']:
            reasoning += f"**Moving Averages:** Price below key support levels. This confirms downtrend. Breaking below moving averages often triggers further selling.\n\n"
        
        if 'volume' in indicators and 'LOW' in indicators['volume']['signal']:
            reasoning += f"**Volume:** {indicators['volume']['change_pct']:.1f}% below average. Low volume during price moves suggests weak conviction and potential reversal.\n\n"
        
        reasoning += f"**📉 Bottom Line:** With {bearish_count}/{total_signals} bearish signals and score below {score}, risk significantly outweighs potential reward. Better opportunities elsewhere.\n"
        
    else:  # HOLD
        reasoning += "**⏸️ Mixed Signals - No Clear Edge:**\n\n"
        reasoning += f"The score of {score}/100 falls in the neutral zone. Here's the dilemma:\n\n"
        
        reasoning += f"**Bullish factors ({bullish_count}):**\n"
        if 'macd' in indicators and 'BULLISH' in indicators['macd']['signal']:
            reasoning += f"- MACD showing positive momentum\n"
        if 'volume' in indicators and 'HIGH' in indicators['volume']['signal']:
            reasoning += f"- Strong volume confirms participation\n"
        if 'bollinger' in indicators and 'ABOVE' in indicators['bollinger']['signal']:
            reasoning += f"- Price above middle Bollinger Band\n"
        
        reasoning += f"\n**Bearish/Neutral factors ({bearish_count + neutral_count}):**\n"
        if 'rsi' in indicators and 40 <= indicators['rsi']['value'] <= 60:
            reasoning += f"- RSI neutral (~{indicators['rsi']['value']:.0f}) - no clear bias\n"
        if 'sma' in indicators and 'INSUFFICIENT' in indicators['sma']['signal']:
            reasoning += f"- Trend unclear (insufficient data)\n"
        
        reasoning += f"\n**⚖️ Bottom Line:** Not enough bullish confirmation to justify entry, but not bearish enough to avoid completely. Wait for {score + 10}-{score + 15} score (clearer setup) or {score - 10}-{score - 15} (clear avoidance). Patience beats forcing trades.\n"
    
    return reasoning


def generate_bull_reasoning(scenarios: dict, indicators: dict) -> str:
    """Generate reasoning for bull case."""
    bull = scenarios['bull']
    bear = scenarios['bear']
    
    is_more_likely = bull['probability'] > bear['probability']
    
    reasoning = f"### 🟢 Bull Case Analysis\n\n"
    
    # Adjust tone based on probability
    if is_more_likely:
        reasoning += f"**Probability: {bull['probability']:.1f}%** (More likely scenario)\n"
        reasoning += f"**Upside Target:** ${bull['target']:.2f} ({bull['change_pct']:+.1f}%)\n\n"
        reasoning += "📈 **Why this scenario is favored:**\n\n"
    else:
        reasoning += f"**Probability: {bull['probability']:.1f}%** (Less likely, but possible)\n"
        reasoning += f"**Upside Target:** ${bull['target']:.2f} ({bull['change_pct']:+.1f}%)\n\n"
        reasoning += "📊 **What would need to happen:**\n\n"
    
    # Count bullish indicators
    bullish_count = 0
    bullish_factors = []
    
    if 'rsi' in indicators:
        rsi = indicators['rsi']['value']
        if rsi < 40:
            bullish_factors.append(f"**RSI Oversold ({rsi:.1f}):** Significant bounce potential from oversold levels. Historically, RSI below 40 sees reversals within 1-5 days in ~65% of cases.")
            bullish_count += 1
        elif rsi < 55:
            bullish_factors.append(f"**RSI Neutral ({rsi:.1f}):** Room to appreciate without hitting overbought resistance at 70. Can sustain upward momentum.")
            bullish_count += 1
    
    if 'macd' in indicators and indicators['macd']['signal'] == 'BULLISH':
        bullish_factors.append(f"**MACD Crossover:** Bullish momentum confirmed. Histogram at {indicators['macd']['histogram']:.2f} shows acceleration. Short-term trend now outpacing long-term, which typically continues for 3-7 days.")
        bullish_count += 1
    
    if 'bollinger' in indicators:
        bb = indicators['bollinger']
        if 'LOWER' in bb['signal']:
            potential = ((bb['middle'] - bb['current']) / bb['current'] * 100)
            bullish_factors.append(f"**Bollinger Band Reversion:** Price near lower band (${bb['lower']:.2f}). Mean reversion to middle band (${bb['middle']:.2f}) would yield {potential:.1f}% gain. Statistically, 70% of touches revert.")
            bullish_count += 1
        elif 'ABOVE' in bb['signal']:
            bullish_factors.append(f"**Bollinger Bands:** Price above middle confirms uptrend. Bulls in control.")
            bullish_count += 1
    
    if 'sma' in indicators and 'BULLISH' in indicators['sma']['signal']:
        bullish_factors.append(f"**Moving Average Support:** Price trading above SMA 50 (${indicators['sma']['sma_50']:.2f}). This acts as support level and confirms trend direction.")
        bullish_count += 1
    
    if 'volume' in indicators and 'HIGH' in indicators['volume']['signal']:
        bullish_factors.append(f"**Volume Confirmation:** {indicators['volume']['change_pct']:+.1f}% above average. Institutional buying or retail FOMO supports sustainable move, not just noise.")
        bullish_count += 1
    
    # Add factors
    for i, factor in enumerate(bullish_factors, 1):
        reasoning += f"{i}. {factor}\n\n"
    
    if not bullish_factors:
        reasoning += "*No strong bullish catalysts detected currently. This scenario relies on external factors (news, sector rotation, market sentiment shift) rather than technical setup.*\n\n"
    
    # Conclusion based on probability
    reasoning += "---\n\n"
    if is_more_likely:
        reasoning += f"**✅ Verdict:** {bullish_count}/5 technical factors support upside. Monte Carlo simulation ({bull['probability']:.1f}% probability) confirms this as the **primary scenario**. "
        if bull['change_pct'] > 2:
            reasoning += f"Target of {bull['change_pct']:+.1f}% offers solid risk/reward."
        else:
            reasoning += f"Modest {bull['change_pct']:+.1f}% target suggests limited upside - manage expectations."
    else:
        reasoning += f"**⚠️ Verdict:** Only {bullish_count}/5 factors support upside. {bull['probability']:.1f}% probability makes this the **secondary scenario**. While possible, "
        reasoning += f"the odds favor the bear case. Would need stronger confirmation (more bullish signals) to justify betting on this outcome."
    
    reasoning += f"\n\n*{bull['description']}*\n"
    
    return reasoning


def generate_bear_reasoning(scenarios: dict, indicators: dict) -> str:
    """Generate reasoning for bear case."""
    bear = scenarios['bear']
    bull = scenarios['bull']
    
    is_more_likely = bear['probability'] > bull['probability']
    
    reasoning = f"### 🔴 Bear Case Analysis\n\n"
    
    # Adjust tone based on probability
    if is_more_likely:
        reasoning += f"**Probability: {bear['probability']:.1f}%** (More likely scenario)\n"
        reasoning += f"**Downside Risk:** ${bear['target']:.2f} ({bear['change_pct']:.1f}%)\n\n"
        reasoning += "📉 **Why this scenario is favored:**\n\n"
    else:
        reasoning += f"**Probability: {bear['probability']:.1f}%** (Less likely, but still a risk)\n"
        reasoning += f"**Downside Risk:** ${bear['target']:.2f} ({bear['change_pct']:.1f}%)\n\n"
        reasoning += "⚠️ **Risk factors to monitor:**\n\n"
    
    # Count bearish indicators
    bearish_count = 0
    bearish_factors = []
    
    if 'rsi' in indicators:
        rsi = indicators['rsi']['value']
        if rsi > 70:
            bearish_factors.append(f"**RSI Overbought ({rsi:.1f}):** Extreme overbought. RSI above 70 typically precedes 2-5% pullbacks within days. Stock is statistically \"expensive\" and due for mean reversion.")
            bearish_count += 1
        elif rsi > 60:
            bearish_factors.append(f"**RSI Elevated ({rsi:.1f}):** Approaching overbought zone. Limited room to run before hitting resistance at 70. Any negative catalyst could trigger selling.")
            bearish_count += 1
    
    if 'macd' in indicators and indicators['macd']['signal'] == 'BEARISH':
        bearish_factors.append(f"**MACD Bearish Crossover:** Momentum turned negative. Histogram at {indicators['macd']['histogram']:.2f} shows deceleration. Short-term trend now underperforming long-term - classic topping signal.")
        bearish_count += 1
    
    if 'bollinger' in indicators:
        bb = indicators['bollinger']
        if 'UPPER' in bb['signal']:
            potential_drop = ((bb['current'] - bb['middle']) / bb['current'] * 100)
            bearish_factors.append(f"**Bollinger Band Extension:** Price at upper band (${bb['upper']:.2f}). Mean reversion to middle (${bb['middle']:.2f}) would mean {potential_drop:.1f}% decline. Price has stretched too far from average.")
            bearish_count += 1
    
    if 'sma' in indicators and 'BEARISH' in indicators['sma']['signal']:
        bearish_factors.append(f"**Moving Average Breakdown:** Price below SMA 50 (${indicators['sma']['sma_50']:.2f}). Lost key support. Traders use this as stop-loss level, triggering cascading selling.")
        bearish_count += 1
    
    if 'volume' in indicators:
        vol = indicators['volume']
        if 'LOW' in vol['signal'] or vol['change_pct'] < -20:
            bearish_factors.append(f"**Volume Weakness:** {vol['change_pct']:.1f}% below average. Low conviction in current price. Moves without volume often reverse quickly.")
            bearish_count += 1
    
    # Add factors
    for i, factor in enumerate(bearish_factors, 1):
        reasoning += f"{i}. {factor}\n\n"
    
    if not bearish_factors:
        reasoning += "*No strong bearish signals detected. This scenario would require external shock (bad news, sector weakness, market crash) rather than technical deterioration.*\n\n"
    
    # Conclusion based on probability
    reasoning += "---\n\n"
    if is_more_likely:
        reasoning += f"**🚨 Verdict:** {bearish_count}/5 technical factors point to downside risk. Monte Carlo simulation ({bear['probability']:.1f}% probability) confirms this as the **primary scenario**. "
        if abs(bear['change_pct']) > 2:
            reasoning += f"Potential {bear['change_pct']:.1f}% drop is significant - risk management critical."
        else:
            reasoning += f"Modest {bear['change_pct']:.1f}% downside, but still the more likely path."
        reasoning += " Consider waiting for better entry or tightening stop-losses."
    else:
        reasoning += f"**✅ Verdict:** Only {bearish_count}/5 factors suggest downside. {bear['probability']:.1f}% probability makes this the **secondary scenario**. "
        reasoning += f"While risk exists, the odds favor the bull case. Monitor these factors but don't let fear override favorable setup. "
        reasoning += "Use stop-loss below key support to protect against this outcome."
    
    reasoning += f"\n\n*{bear['description']}*\n"
    
    return reasoning


def display_summary(stock_info: dict, score_results: dict, scenarios: dict, timeframe: str, indicators: dict):
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
    
    # NEW: "Why?" button for signal
    with st.expander("❓ **Why this signal?** (Click to see reasoning)", expanded=False):
        signal_reasoning = generate_signal_reasoning(score_results, indicators, stock_info)
        st.markdown(signal_reasoning)
    
    # Bull and Bear scenarios
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🟢 BULL CASE")
        bull = scenarios['bull']
        st.markdown(f"**Probability:** {bull['probability']:.1f}%")
        st.markdown(bull['description'])
        
        # NEW: "Why?" button for bull case
        with st.expander("❓ **Why bullish?**", expanded=False):
            bull_reasoning = generate_bull_reasoning(scenarios, indicators)
            st.markdown(bull_reasoning)
    
    with col2:
        st.markdown("### 🔴 BEAR CASE")
        bear = scenarios['bear']
        st.markdown(f"**Probability:** {bear['probability']:.1f}%")
        st.markdown(bear['description'])
        
        # NEW: "Why?" button for bear case
        with st.expander("❓ **Why bearish?**", expanded=False):
            bear_reasoning = generate_bear_reasoning(scenarios, indicators)
            st.markdown(bear_reasoning)


def display_detailed_analysis(indicators: dict, score_results: dict, stock_info: dict):
    """Display detailed technical analysis."""
    st.markdown("---")
    st.markdown("## 📈 DETAILED TECHNICAL ANALYSIS")
    
    with st.expander("📊 Technical Indicators Breakdown", expanded=True):
        # RSI
        if 'rsi' in indicators:
            col_title, col_info = st.columns([11, 1])
            with col_title:
                st.markdown("### RSI (Relative Strength Index)")
            with col_info:
                with st.popover("ℹ️", use_container_width=False):
                    st.markdown("""
                    **What is RSI?**
                    
                    The Relative Strength Index (RSI) measures the speed and magnitude of recent price changes to evaluate overbought or oversold conditions.
                    
                    **Range:** 0-100
                    - **< 30:** Oversold (may bounce up)
                    - **30-70:** Neutral zone
                    - **> 70:** Overbought (may pull back)
                    
                    **How to use:**
                    - RSI < 30 often signals buying opportunity
                    - RSI > 70 suggests caution (potential reversal)
                    - Divergences (price vs RSI) can predict reversals
                    """)
            
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
            col_title, col_info = st.columns([11, 1])
            with col_title:
                st.markdown("### MACD (Moving Average Convergence Divergence)")
            with col_info:
                with st.popover("ℹ️", use_container_width=False):
                    st.markdown("""
                    **What is MACD?**
                    
                    MACD shows the relationship between two moving averages to identify momentum changes and trend direction.
                    
                    **Components:**
                    - **MACD Line:** 12-day EMA minus 26-day EMA
                    - **Signal Line:** 9-day EMA of MACD Line
                    - **Histogram:** MACD Line minus Signal Line
                    
                    **Signals:**
                    - **Golden Cross:** MACD crosses above Signal → Bullish
                    - **Death Cross:** MACD crosses below Signal → Bearish
                    - **Histogram widening:** Strengthening momentum
                    - **Histogram narrowing:** Weakening momentum
                    
                    **How to use:**
                    - Look for crossovers as entry/exit signals
                    - Histogram shows momentum strength
                    - Best combined with other indicators
                    """)
            
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
            col_title, col_info = st.columns([11, 1])
            with col_title:
                st.markdown("### Bollinger Bands")
            with col_info:
                with st.popover("ℹ️", use_container_width=False):
                    st.markdown("""
                    **What are Bollinger Bands?**
                    
                    Bollinger Bands measure volatility and identify overbought/oversold conditions using standard deviations around a moving average.
                    
                    **Components:**
                    - **Middle Band:** 20-day Simple Moving Average (SMA)
                    - **Upper Band:** Middle + (2 × standard deviation)
                    - **Lower Band:** Middle - (2 × standard deviation)
                    
                    **Signals:**
                    - **Price at Upper Band:** Overbought (potential reversal down)
                    - **Price at Lower Band:** Oversold (potential bounce up)
                    - **Price above Middle:** Bullish trend
                    - **Price below Middle:** Bearish trend
                    - **Band Squeeze:** Low volatility, breakout coming
                    - **Band Expansion:** High volatility, trend in motion
                    
                    **Mean Reversion:**
                    When price touches a band, it often reverts back to the middle band (~70% of the time statistically).
                    """)
            
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
            col_title, col_info = st.columns([11, 1])
            with col_title:
                st.markdown("### Simple Moving Averages (SMA)")
            with col_info:
                with st.popover("ℹ️", use_container_width=False):
                    st.markdown("""
                    **What are SMAs?**
                    
                    Simple Moving Averages smooth out price data to identify trend direction and support/resistance levels.
                    
                    **Common Periods:**
                    - **SMA 50:** Short-term trend (50 trading days ≈ 2.5 months)
                    - **SMA 200:** Long-term trend (200 trading days ≈ 10 months)
                    
                    **Signals:**
                    - **Price above SMA 50:** Short-term uptrend
                    - **Price below SMA 50:** Short-term downtrend
                    - **Price above SMA 200:** Long-term bull market
                    - **Price below SMA 200:** Long-term bear market
                    
                    **Golden Cross vs Death Cross:**
                    - **Golden Cross:** SMA 50 crosses above SMA 200 → Very bullish
                    - **Death Cross:** SMA 50 crosses below SMA 200 → Very bearish
                    
                    **Support/Resistance:**
                    SMAs often act as dynamic support (in uptrends) or resistance (in downtrends). Price bounces off them frequently.
                    """)
            
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
            col_title, col_info = st.columns([11, 1])
            with col_title:
                st.markdown("### Volume Analysis")
            with col_info:
                with st.popover("ℹ️", use_container_width=False):
                    st.markdown("""
                    **What is Volume?**
                    
                    Volume represents the total number of shares traded in a given period. It confirms the strength of price movements.
                    
                    **Key Concepts:**
                    - **High Volume:** Strong conviction, validates price moves
                    - **Low Volume:** Weak participation, moves may reverse
                    - **Volume Spike:** Unusual activity, often precedes major moves
                    
                    **Volume Patterns:**
                    - **Price up + Volume up:** Strong bullish confirmation
                    - **Price up + Volume down:** Weak rally, may fail
                    - **Price down + Volume up:** Strong selling pressure
                    - **Price down + Volume down:** Weak decline, may bounce
                    
                    **Why it matters:**
                    Volume confirms whether price movements are supported by real buying/selling or just noise. Without volume, price moves lack conviction.
                    
                    **Average Volume:**
                    Compared to 20-day average to identify unusual activity.
                    """)
            
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
            display_summary(stock_info, score_results, scenarios, timeframe_display, indicators)
            
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
