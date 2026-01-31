# Stock Analysis Bot - Final Specification

**Version:** 1.0  
**Date:** 2026-01-31  
**Status:** ✅ Ready to Build

---

## 🎯 User Flow

### Step 1: Disclaimer & Risk Acceptance (First Time Only)

```
╔═══════════════════════════════════════════════════════╗
║  ⚠️  IMPORTANT DISCLAIMER                             ║
╠═══════════════════════════════════════════════════════╣
║                                                       ║
║  This tool provides EDUCATIONAL analysis only.        ║
║                                                       ║
║  ❌ NOT financial advice                             ║
║  ❌ NOT investment recommendations                   ║
║                                                       ║
║  ✅ Always do your own research                      ║
║  ✅ Consult a licensed financial advisor             ║
║                                                       ║
║  ⚠️  Trading involves significant risk of loss.      ║
║  📉 Past performance ≠ future results                ║
║                                                       ║
║  By continuing, you acknowledge:                      ║
║  ☐ This is for educational purposes only             ║
║  ☐ I understand the risk of financial loss           ║
║  ☐ I will not hold creators liable for losses        ║
║                                                       ║
║  [ I Understand & Accept ]  [ Cancel ]               ║
╚═══════════════════════════════════════════════════════╝
```

**Storage:** Cookie/LocalStorage speichert Acceptance (30 Tage gültig)

---

### Step 2: Analysis Input

```
╔═══════════════════════════════════════════════════════╗
║  📊 Stock Analysis Tool                               ║
╠═══════════════════════════════════════════════════════╣
║                                                       ║
║  Enter Stock Ticker:                                  ║
║  [AAPL________________]  🔍                          ║
║                                                       ║
║  ⏱️ Trading Timeframe:                               ║
║  ◉ Short-term (1-7 days)                             ║
║  ○ Medium-term (1-4 weeks)                           ║
║  ○ Long-term (1-6 months)                            ║
║                                                       ║
║  🎲 Risk Tolerance:                                   ║
║  ○ Conservative (high confidence only)                ║
║  ◉ Moderate (balanced)                               ║
║  ○ Aggressive (speculative plays OK)                 ║
║                                                       ║
║  [ Analyze Stock ]                                    ║
║                                                       ║
║  ⚠️ Educational use only - Not financial advice      ║
╚═══════════════════════════════════════════════════════╝
```

---

### Step 3: Analysis Output

## 📊 **SUMMARY VIEW** (Top of Page)

```
═══════════════════════════════════════════════════════
📊 AAPL - Apple Inc.                    $185.32 (+2.4%)
═══════════════════════════════════════════════════════

🎯 SIGNAL: BUY                          Score: 72/100
💪 CONFIDENCE: High (85%)                🕐 Short-term
⏰ Updated: 2026-01-31 12:05 UTC

───────────────────────────────────────────────────────
🟢 BULL CASE (Probability: 65%)
───────────────────────────────────────────────────────
Target: $195 (+5.2%) in 5-7 days

Key Factors:
• RSI oversold (28) → rebound likely
• MACD golden cross forming
• Bounced off lower Bollinger Band
• Strong volume spike (+40%)

───────────────────────────────────────────────────────
🔴 BEAR CASE (Probability: 35%)
───────────────────────────────────────────────────────
Risk: $175 (-5.6%) if support breaks

Risk Factors:
• Market VIX elevated (32)
• High P/E ratio (32.5 vs. sector 18)
• Macro uncertainty (Fed meeting next week)

───────────────────────────────────────────────────────
💡 RECOMMENDATION
───────────────────────────────────────────────────────
Action: BUY (small position)
Entry: $184-186
Target: $195
Stop-Loss: $180
Position Size: 2-5% of portfolio (conservative)

Risk/Reward: 1:2.5 (favorable)

───────────────────────────────────────────────────────
[ 📄 View Detailed Analysis ] [ 📊 View Charts ]
═══════════════════════════════════════════════════════
```

---

## 📄 **DETAILED VIEW** (Expandable/Below Summary)

### Section 1: Technical Indicators (Detailed)

```
═══════════════════════════════════════════════════════
📈 TECHNICAL INDICATORS
═══════════════════════════════════════════════════════

RSI (14-period): 28.4 → OVERSOLD ✅
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Score: +20/20
Signal: Strong BUY
Interpretation: Heavily oversold. Historical rebounds 
from RSI<30 occur 78% of time within 5 days.

─────────────────────────────────────────────────────

MACD:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MACD Line: 2.34
Signal Line: 2.18
Histogram: +0.16 (widening)

Score: +25/25
Signal: BULLISH (Golden Cross forming)
Interpretation: MACD crossed above signal line 2 days 
ago. Momentum building. Histogram widening = strength.

─────────────────────────────────────────────────────

Bollinger Bands (20-period, 2σ):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Upper Band: $195.20
Middle (SMA): $188.50
Lower Band: $181.80
Current: $185.32

Score: +10/15
Signal: NEAR LOWER BAND (mean reversion setup)
Interpretation: Price touched lower band yesterday, 
now +$3.50 off bottom. Classic rebound setup.

─────────────────────────────────────────────────────

SMA (50/200):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
50-day SMA: $190.45
200-day SMA: $178.30
Current: $185.32

Score: +10/20
Signal: NEUTRAL (between 50 & 200)
Interpretation: Above 200-day (bullish long-term), 
below 50-day (short-term weakness). No golden/death cross.

─────────────────────────────────────────────────────

Volume:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Today: 85.2M shares
20-day avg: 60.8M shares
Difference: +40.1%

Score: +10/10
Signal: STRONG VOLUME (confirmation)
Interpretation: Volume spike on bounce = buyers 
stepping in. Validates reversal signal.

─────────────────────────────────────────────────────

🎯 TOTAL TECHNICAL SCORE: 75/100 → BUY
```

---

### Section 2: Probabilistic Analysis

```
═══════════════════════════════════════════════════════
🎲 MONTE CARLO SIMULATION (1000 iterations)
═══════════════════════════════════════════════════════

Simulation Parameters:
• Drift: 0.12% daily (based on 60-day average)
• Volatility: 1.8% daily (historical)
• Starting Price: $185.32
• Timeframe: 7 trading days

Results:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Probability Distribution (7 days):

65% → $190 - $200  (BULLISH)
20% → $180 - $190  (NEUTRAL)
15% → $170 - $180  (BEARISH)

Expected Value (Median): $191.20 (+3.2%)
Mean: $192.50 (+3.9%)
10th Percentile: $177.50 (-4.2%)
90th Percentile: $203.80 (+10.0%)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Bayesian Update (if new data arrives):
• If volume continues high → P(bullish) 65% → 72%
• If support breaks → P(bearish) 35% → 58%

[Show Monte Carlo Chart]
```

---

### Section 3: Market Context

```
═══════════════════════════════════════════════════════
🌐 MARKET CONTEXT
═══════════════════════════════════════════════════════

VIX (Volatility Index): 32.4 (+8.2%)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Interpretation: ELEVATED FEAR
VIX > 30 = Market stress. Historically, creates 
dip-buying opportunities but requires caution.

─────────────────────────────────────────────────────

SPY (S&P 500): -1.2% today
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Correlation with AAPL: 0.78 (high)
Interpretation: Market headwind. AAPL outperforming 
(+2.4% vs. -1.2%) = relative strength.

─────────────────────────────────────────────────────

Sector Performance (Technology):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
XLK (Tech ETF): -0.8%
Interpretation: Tech sector weak, but AAPL stronger.
```

---

### Section 4: Fundamental Snapshot (Long-term only)

```
═══════════════════════════════════════════════════════
💼 FUNDAMENTALS (for Long-term analysis)
═══════════════════════════════════════════════════════

P/E Ratio: 32.5 (vs. sector avg: 18.2) → EXPENSIVE
EPS (TTM): $6.42
Revenue Growth (YoY): +8.2%
Profit Margin: 25.1%

Recent SEC Filings:
• 10-K filed: 2025-11-02 (clean)
• 13F changes: Berkshire increased position (+2.4M shares)

Next Earnings: 2026-02-15 (15 days)
```

---

### Section 5: News Sentiment (if available)

```
═══════════════════════════════════════════════════════
📰 NEWS SENTIMENT (Last 24h)
═══════════════════════════════════════════════════════

Overall Sentiment: NEUTRAL (52% positive)

Recent Headlines:
• "Apple announces new AI features" (+) - 4h ago
• "Tech stocks tumble on Fed concerns" (-) - 8h ago
• "AAPL beats sales estimates in China" (+) - 12h ago

Sentiment Score: 5.2/10 (slightly bullish)
```

---

## 🎨 UI Mock (Web App)

### **Top Section - Summary Card:**
- Big, clear BUY/SELL/HOLD
- Score + Confidence
- Quick Bull/Bear with probabilities
- Recommendation

### **Expandable Sections:**
- 📈 Technical Indicators (full breakdown)
- 🎲 Monte Carlo Simulation (chart + stats)
- 🌐 Market Context (VIX, SPY, Sector)
- 💼 Fundamentals (if long-term selected)
- 📰 News Sentiment
- 📊 Charts (interactive)

### **Settings Panel (Top Right):**
```
⚙️ Settings
├─ Timeframe: [Short ▼] [Medium] [Long]
├─ Risk: [Conservative] [Moderate ▼] [Aggressive]
└─ View: [Summary + Details ✓]
```

---

## 📊 Scoring Models (Timeframe-Dependent)

### **SHORT-TERM (1-7 days):**

| Indicator | Weight | Reasoning |
|-----------|--------|-----------|
| RSI | 25 pts | Critical for oversold/overbought |
| MACD | 30 pts | Momentum king for short-term |
| Bollinger Bands | 20 pts | Mean reversion setups |
| Volume | 15 pts | Confirmation needed |
| SMA | 10 pts | Less important short-term |
| **TOTAL** | **100 pts** | |

**Thresholds:**
- 80-100: STRONG BUY
- 65-79: BUY
- 45-64: HOLD
- 30-44: SELL
- 0-29: STRONG SELL

---

### **MEDIUM-TERM (1-4 weeks):**

| Indicator | Weight | Reasoning |
|-----------|--------|-----------|
| MACD | 25 pts | Trend confirmation |
| SMA (50/200) | 25 pts | Trend direction |
| RSI | 20 pts | Entry timing |
| Bollinger Bands | 15 pts | Volatility context |
| Volume | 10 pts | Support/resistance breaks |
| Sentiment | 5 pts | News catalyst |
| **TOTAL** | **100 pts** | |

---

### **LONG-TERM (1-6 months):**

| Indicator | Weight | Reasoning |
|-----------|--------|-----------|
| SMA (50/200) | 30 pts | Primary trend |
| Fundamentals | 25 pts | Valuation, growth |
| SEC Filings | 15 pts | Insider/institutional activity |
| MACD | 15 pts | Momentum |
| RSI | 10 pts | Timing |
| Sentiment | 5 pts | Long-term narrative |
| **TOTAL** | **100 pts** | |

---

## 🎲 Risk Tolerance Impact

### **Conservative:**
**Characteristics:**
- Only signals with >75% confidence
- Narrow entry ranges
- Strict stop-losses
- Small position sizes (2-3%)

**Signal Adjustments:**
- BUY (72 score) + Medium Confidence → **HOLD** (wait for better setup)
- STRONG BUY (85) + High Confidence → **BUY** (proceed cautiously)

**Output Changes:**
- Emphasize risks more
- Conservative position sizing
- Tighter stop-losses

---

### **Moderate:** (Default)
**Characteristics:**
- Signals with >60% confidence
- Balanced risk/reward
- Standard position sizes (3-7%)

**Signal Adjustments:**
- Score as-is
- Standard recommendations

---

### **Aggressive:**
**Characteristics:**
- Accept >50% confidence
- Wider entry ranges
- Larger position sizes (5-10%)
- Higher risk/reward setups

**Signal Adjustments:**
- BUY (65) + Medium Confidence → **STRONG BUY** (go bigger)
- Show speculative plays (options strategies, high-vol stocks)

**Output Changes:**
- Show "High Risk/High Reward" scenarios
- Larger position size recommendations
- Mention leveraged plays (optional)

---

## 📊 Output Example (Complete)

```
╔════════════════════════════════════════════════════════════════╗
║  📊 STOCK ANALYSIS                                             ║
╠════════════════════════════════════════════════════════════════╣
║  AAPL - Apple Inc.                          $185.32  (+2.4%)  ║
║  Updated: 2026-01-31 12:05 UTC             Volume: 85.2M      ║
╚════════════════════════════════════════════════════════════════╝

═══════════════════════════════════════════════════════════════
                    📋 SUMMARY
═══════════════════════════════════════════════════════════════

🎯 SIGNAL: BUY                          Score: 72/100 ⭐⭐⭐⭐☆
💪 CONFIDENCE: High (85%)                Timeframe: Short-term
🎲 RISK LEVEL: Moderate

───────────────────────────────────────────────────────────────
🟢 BULL CASE                           Probability: 65%
───────────────────────────────────────────────────────────────
Target: $195 (+5.2%) in 5-7 days

Top Factors:
 ✓ RSI oversold (28)
 ✓ MACD golden cross
 ✓ Bollinger bounce
 ✓ Volume spike (+40%)
 ✓ Support held at $183

Scenario: Technical rebound setup. If $183 support holds,
expect move to $190-195 within a week.

───────────────────────────────────────────────────────────────
🔴 BEAR CASE                           Probability: 35%
───────────────────────────────────────────────────────────────
Risk: $175 (-5.6%) if support breaks

Risk Factors:
 ⚠ VIX elevated (32)
 ⚠ High valuation (P/E 32.5)
 ⚠ Market uncertainty
 ⚠ Weak sector performance

Scenario: If $183 breaks on high volume, sell-off
accelerates to next support at $175.

───────────────────────────────────────────────────────────────
💡 RECOMMENDATION (Moderate Risk Tolerance)
───────────────────────────────────────────────────────────────
Action: BUY (small position)
Entry: $184-$186
Target: $195
Stop-Loss: $180 (hard stop)
Position Size: 3-5% of portfolio

Risk/Reward Ratio: 1:2.5 (favorable)

Rationale: Technical setup favors upside, but macro 
risk exists. Conservative sizing recommended.

═══════════════════════════════════════════════════════════════
                [ View Detailed Analysis ▼ ]
═══════════════════════════════════════════════════════════════
```

**When expanded (▼):**

All sections from above:
- Full Technical Indicators breakdown
- Monte Carlo Simulation details
- Market Context
- Fundamentals (if long-term)
- News Sentiment
- Interactive Charts

---

## 🔄 Dynamic Adjustments

### **Timeframe Changes Scoring:**

**Short-term selected:**
- RSI weight: 25%
- MACD weight: 30%
- Volume critical

**Long-term selected:**
- Fundamentals weight: 25%
- SMA weight: 30%
- SEC filings important

### **Risk Tolerance Changes Output:**

**Conservative:**
- Show: "Wait for better entry"
- Position size: 2-3%
- Stop-loss: Tight (-2%)

**Aggressive:**
- Show: "High risk/reward play"
- Position size: 7-10%
- Stop-loss: Wider (-5%)

---

## 🛠️ Technical Implementation

### Data Flow:
```
User Input (Ticker + Timeframe + Risk)
    ↓
Fetch Data (yfinance, Alpha Vantage)
    ↓
Calculate Indicators (pandas-ta)
    ↓
Apply Scoring Model (timeframe-dependent)
    ↓
Run Monte Carlo (numpy)
    ↓
Generate Bull/Bear Scenarios (GPT-assist optional)
    ↓
Format Output (Summary + Details)
    ↓
Display with Charts (Chart.js)
```

---

## 📦 MVP Features (Week 1)

**Must-Have:**
- ✅ Ticker input
- ✅ Timeframe selector (3 options)
- ✅ Risk tolerance selector (3 options)
- ✅ Disclaimer + acceptance
- ✅ Technical indicators (RSI, MACD, Bollinger, SMA, Volume)
- ✅ Scoring system (timeframe-dependent)
- ✅ Bull/Bear scenarios
- ✅ Summary + detailed view
- ✅ Basic charts (price + indicators)
- ✅ BUY/SELL/HOLD recommendation

**Nice-to-Have (if time):**
- ⚠️ Monte Carlo simulation
- ⚠️ News sentiment (basic)
- ⚠️ SEC filing check

---

## ⚠️ Legal/Compliance

**Every Page Must Have:**
```
⚠️ DISCLAIMER: Educational use only. Not financial advice.
Past performance does not guarantee future results.
Trading involves risk of loss.
```

**Footer:**
```
This tool is for educational and informational purposes only.
It does not constitute financial, investment, or trading advice.
Always consult a licensed financial advisor before making investment decisions.
The creators are not liable for any financial losses incurred.
```

---

## 🚀 Ready to Build?

**All decisions made:**
- ✅ Scoring system defined
- ✅ Timeframe as user selection
- ✅ Risk tolerance as user selection
- ✅ Output format: Summary + Details
- ✅ Free tier data sources
- ✅ Disclaimer flow designed

**Next:** Start building!

**Estimated Timeline:**
- Day 1-2: Backend (data fetching, indicators, scoring)
- Day 3-4: Frontend (UI, forms, display)
- Day 5: Monte Carlo + charts
- Day 6-7: Polish + deployment

**Ready when you are!** 🚀📊
