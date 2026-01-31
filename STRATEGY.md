# Stock Analysis Bot - Strategy & Requirements

**Updated:** 2026-01-31  
**Status:** Ready to build

---

## 🎯 Core Requirements (Final)

### 1. **Scoring System** ✅

**Weighted Indicator Scoring (0-100 Points):**

```
Technical Indicators:
├─ RSI (0-20 pts)
│  └─ <30: +20 (oversold), >70: -20 (overbought), 40-60: 0
├─ MACD (0-25 pts)
│  └─ Golden Cross: +25, Death Cross: -25, Neutral: 0
├─ Bollinger Bands (0-15 pts)
│  └─ Price < Lower Band: +15, Price > Upper Band: -15
├─ SMA (50/200) (0-20 pts)
│  └─ Golden Cross: +20, Death Cross: -20, Above both: +10
└─ Volume (0-10 pts)
   └─ Above average: +10, Below: -5

Momentum (0-10 pts):
└─ Stochastic: <20: +10, >80: -10

Total Score → Signal:
  80-100: STRONG BUY
  60-79:  BUY
  40-59:  HOLD
  20-39:  SELL
  0-19:   STRONG SELL
```

**Confidence Score:**
- Based on signal agreement (all indicators aligned → high confidence)
- Number of confirming indicators
- Volatility (high vol → lower confidence)

---

### 2. **Timeframe Filter** ✅

**User wählt beim Start:**

#### Option A: **Kurzfristig (1-7 Tage)**
**Fokus:** Day Trading, Swing Trading

**Indicators weighted differently:**
- RSI: Heavy weight (25 pts)
- MACD: Heavy (30 pts)
- Bollinger Bands: Heavy (20 pts)
- Volume: Important (15 pts)
- SMA: Lower (10 pts)

**Additional:**
- Intraday volatility analysis
- Recent news sentiment (last 24h)
- Tick Index (market sentiment)

**Output:**
- "Short-term momentum suggests..."
- Entry/Exit price ranges
- Stop-loss recommendations

---

#### Option B: **Langfristig (4+ Wochen)**
**Fokus:** Position Trading, Investing

**Indicators weighted differently:**
- SMA (50/200): Heavy (30 pts)
- MACD: Medium (20 pts)
- RSI: Medium (15 pts)
- Fundamentals: Heavy (25 pts)
- SEC Filings: Important (10 pts)

**Additional:**
- P/E Ratio analysis
- Earnings trends (quarterly)
- SEC 13D/13F filing changes
- Industry comparison

**Output:**
- "Long-term outlook based on..."
- Target price (3-6 months)
- Fundamental health score

---

### 3. **Free Tier Data Sources** ✅

**Primary:**
- **yfinance** (Yahoo Finance) - Price data, historical, volume
- **SEC EDGAR API** - Filings (13D, 13F, 8-K, 10-K)
- **Alpha Vantage Free** (500 calls/day) - Technical indicators
- **News API Free** (100 calls/day) - Headlines

**What we CAN'T get (Premium only):**
- ❌ Real-time Order Book (Level 2 data)
- ❌ Options Flow
- ❌ Advanced sentiment (Bloomberg, Reuters)
- ❌ Institutional ownership changes (real-time)

**Workarounds:**
- Use delayed data (15-20 min is OK for most analysis)
- Estimate sentiment from free news headlines
- Use SEC filings (delayed but official)

---

### 4. **Separate Bull/Bear Scenarios** ✅

**Output Format:**

```markdown
## 📊 Analysis: AAPL (2026-01-31)

**Current Price:** $185.32 (+2.4%)  
**Signal:** BUY (Score: 72/100)  
**Confidence:** High (85%)  
**Timeframe:** Short-term (1-7 days)

---

### 🟢 BULL CASE (Probability: 65%)

**Target Price:** $195 (+5.2%)  
**Timeline:** 5-7 trading days

**Supporting Factors:**
1. RSI oversold at 28 (rebound likely)
2. MACD forming golden cross
3. Bounced off lower Bollinger Band
4. Positive earnings surprise (+12% vs. estimate)
5. Volume spike on bounce (+40% above avg)

**Scenario:**
If the current support at $183 holds, technical rebound to $190-195 
is likely within 5-7 days. Historical pattern shows 78% success rate 
for similar RSI+MACD setups.

**Entry:** $184-186  
**Target:** $195  
**Stop-Loss:** $180

---

### 🔴 BEAR CASE (Probability: 35%)

**Target Price:** $175 (-5.6%)  
**Timeline:** 3-5 trading days

**Risk Factors:**
1. Market-wide VIX spike (fear rising)
2. High P/E ratio (32.5 vs. industry avg 18)
3. Weak forward guidance from CEO
4. Potential Fed rate hike next week
5. Support at $183 is recent (not tested)

**Scenario:**
If $183 support breaks on high volume, sell-off could accelerate 
to next support at $175. Market uncertainty could override technical 
indicators.

**Risk Level:** Medium  
**Probability of support break:** 35%

---

### ⚙️ **Recommendation:**

**Action:** BUY (small position, 2-5% of portfolio)  
**Rationale:** Technical setup favors bullish, but market risk exists  
**Position Sizing:** Conservative due to macro uncertainty  
**Monitor:** $183 support level closely

---

### 📈 **Monte Carlo Simulation (1000 runs):**
- 65% reach $190+ within 7 days
- 20% stay flat ($180-190)
- 15% drop below $180

**Expected Value:** $191 (median outcome)
```

---

### 5. **Disclaimer & Risk Acknowledgment** ✅

**Flow:**

#### Step 1: First-Time User
```
⚠️ IMPORTANT DISCLAIMER

This tool provides EDUCATIONAL analysis only.

NOT financial advice. NOT investment recommendations.
Always do your own research and consult a licensed advisor.

Trading involves significant risk of loss.
Past performance does not guarantee future results.

☐ I understand this is for educational purposes only
☐ I acknowledge the risk of financial loss
☐ I will not hold the creators liable for losses

[I Understand & Accept] [Cancel]
```

#### Step 2: Every Analysis
```
⚠️ Reminder: This is educational analysis, not financial advice.

Last accepted: 2026-01-31 11:58 UTC

[Proceed with Analysis]
```

**Legal Coverage:**
- Prominent disclaimer on EVERY page
- User must actively check boxes
- Log acceptance (timestamp + IP for liability)
- Clear "Educational Use Only" language

---

## 🏗️ Updated Architecture

### **User Flow:**

```
1. User Input:
   ├─ Ticker Symbol (e.g., AAPL)
   ├─ Timeframe: [Short-term] [Long-term]
   └─ Accept Disclaimer

2. Data Collection:
   ├─ yfinance: Price history, volume
   ├─ Alpha Vantage: Technical indicators (cached)
   └─ SEC EDGAR: Recent filings (if available)

3. Analysis:
   ├─ Calculate Technical Indicators
   ├─ Apply Scoring Model (timeframe-dependent)
   ├─ Run Monte Carlo (1000 iterations)
   └─ Generate Bull/Bear Scenarios

4. Output:
   ├─ Signal: BUY/SELL/HOLD
   ├─ Score: X/100
   ├─ Confidence: High/Medium/Low
   ├─ Bull Case (with probability)
   ├─ Bear Case (with probability)
   ├─ Recommendation (with disclaimers!)
   └─ Charts (price, indicators)
```

---

## 📋 Missing Pieces (Optional - can add later)

These would make it BETTER but not required for MVP:

### Nice-to-Have (Phase 2):
- **Sentiment Analysis** (Real-time news scraping + NLP)
- **Insider Trading** (SEC Form 4 tracking)
- **Options Unusual Activity** (if we find free source)
- **Correlation Analysis** (vs. SPY, sector)
- **Historical Win Rate** (backtest gegen 1 Jahr Daten)

### Advanced (Phase 3):
- **Machine Learning Model** (train on historical patterns)
- **Portfolio Optimization** (multiple stocks)
- **Alerts** (Email/Telegram when signal changes)
- **Watchlist** (track multiple stocks)

---

## ✅ Was wir JETZT bauen können (MVP):

**Mit deinen Infos + diesen Decisions:**

1. ✅ Scoring System (defined above)
2. ✅ Timeframe Filter (Short vs. Long)
3. ✅ Free Tier Data (yfinance + SEC EDGAR)
4. ✅ Separate Bull/Bear Scenarios
5. ✅ Disclaimer + Risk Acceptance
6. ✅ Technical Indicators (MACD, RSI, Bollinger, SMA, Volume)
7. ✅ Monte Carlo (simplified, 1000 iterations)
8. ⚠️ Basic Sentiment (headlines only, keine Deep NLP)

**Das ist ein SOLIDES MVP!** 🚀

---

## ❓ Offene Fragen für dich:

1. **Trading-Stil präferenz:**
   - Eher Day Trading (sehr kurzfristig)?
   - Swing Trading (Tage-Wochen)?
   - Position Trading (Wochen-Monate)?

2. **Risk Level:**
   - Konservativ (nur hohe Confidence-Signale)?
   - Moderat (Balance)?
   - Aggressiv (auch spekulative Signale)?

3. **Output-Format:**
   - Detailliert (alle Daten, Begründungen)?
   - Kompakt (nur Signal + Key Points)?
   - Beides?

---

## 🚀 Next Steps

**Wenn du grünes Licht gibst:**

1. Ich erstelle das vollständige Scoring-Modell
2. Baue die Timeframe-Filter-Logik
3. Implementiere Disclaimer-Flow
4. Erstelle MVP (CLI erst, dann Web-App)

**Soll ich loslegen? Oder hast du noch Input zu den offenen Fragen?** 👇
