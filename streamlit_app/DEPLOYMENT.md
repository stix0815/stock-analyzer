# Deployment Guide - Stock Analysis Streamlit App

## 🚀 Quick Start (Local)

### Option 1: Simple Start
```bash
cd stock_analyzer/streamlit_app
pip install -r requirements.txt
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`

### Option 2: Using Python Module
```bash
cd stock_analyzer/streamlit_app
python3 -m pip install -r requirements.txt
python3 -m streamlit run app.py
```

---

## ☁️ Deploy to Streamlit Cloud (FREE!)

### Prerequisites
- GitHub account
- Streamlit account (free at [share.streamlit.io](https://share.streamlit.io))

### Step-by-Step Deployment

#### 1. Push Code to GitHub
```bash
# Initialize git repo (if not already)
git init

# Add files
git add stock_analyzer/

# Commit
git commit -m "Add stock analysis Streamlit app"

# Create repo on GitHub and push
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

#### 2. Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Select your GitHub repository
4. Set:
   - **Repository:** YOUR_USERNAME/YOUR_REPO
   - **Branch:** main
   - **Main file path:** stock_analyzer/streamlit_app/app.py
5. Click "Deploy!"

⏱️ Deployment takes 2-5 minutes. You'll get a public URL like:
```
https://YOUR-APP-NAME.streamlit.app
```

#### 3. Share Your App!
Your app is now live and accessible to anyone with the URL!

---

## 🐳 Docker Deployment (Optional)

### Create Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Build and Run
```bash
cd stock_analyzer/streamlit_app

# Build image
docker build -t stock-analyzer .

# Run container
docker run -p 8501:8501 stock-analyzer
```

Access at `http://localhost:8501`

---

## 🔧 Configuration Options

### Custom Port
```bash
streamlit run app.py --server.port 8080
```

### Headless Mode (No Browser)
```bash
streamlit run app.py --server.headless true
```

### Custom Theme
Create `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"
```

---

## 📊 Performance Tips

### For Production
1. **Cache Data:** Already implemented with yfinance data fetching
2. **Limit Historical Data:** Adjust timeframe periods in `data_fetcher.py`
3. **Reduce Monte Carlo Iterations:** In `monte_carlo.py`, reduce from 1000 to 500 for faster loading

### Resource Limits
- **Streamlit Cloud Free Tier:**
  - 1 GB RAM
  - 1 CPU core
  - Sufficient for this app with normal traffic

---

## 🔒 Security & Best Practices

### Environment Variables
If adding API keys (future enhancements), use Streamlit secrets:

1. Create `.streamlit/secrets.toml`:
```toml
api_key = "your-secret-key"
```

2. Access in code:
```python
import streamlit as st
api_key = st.secrets["api_key"]
```

3. Add to `.gitignore`:
```
.streamlit/secrets.toml
```

### Rate Limiting
yfinance is free but has rate limits:
- Don't spam requests
- Cache results when possible
- Consider adding request delays for high traffic

---

## 📝 Maintenance

### Update Dependencies
```bash
pip install --upgrade streamlit yfinance pandas numpy plotly scipy
pip freeze > requirements.txt
```

### Monitor Performance
Check Streamlit Cloud dashboard for:
- Active users
- CPU/Memory usage
- Error logs

### Troubleshooting

**App won't start:**
- Check `requirements.txt` has all dependencies
- Verify Python version (3.8+)
- Check error logs in terminal

**Slow performance:**
- Reduce historical data period
- Decrease Monte Carlo iterations
- Check network connection for yfinance

**Data not loading:**
- Verify ticker symbol is valid
- Check yfinance service status
- Try different ticker (AAPL, MSFT, etc.)

---

## 🎨 Customization

### Add Your Branding
In `app.py`, modify:
```python
st.set_page_config(
    page_title="Your Company - Stock Analyzer",
    page_icon="🚀",  # Your icon
)
```

### Custom Disclaimer
Edit disclaimer text in `show_disclaimer()` function in `app.py`

### Additional Features
Consider adding:
- Email alerts
- Portfolio tracking
- News sentiment (requires API)
- Options strategies
- Backtesting

---

## 📈 Monitoring & Analytics

### Streamlit Analytics (Built-in)
- View on Streamlit Cloud dashboard
- See active users, page views
- Monitor errors

### Google Analytics (Optional)
Add to `app.py`:
```python
# Add Google Analytics tag in custom HTML
st.markdown("""
<script async src="https://www.googletagmanager.com/gtag/js?id=YOUR-GA-ID"></script>
""", unsafe_allow_html=True)
```

---

## 🆘 Support Resources

- **Streamlit Docs:** https://docs.streamlit.io
- **yfinance Docs:** https://pypi.org/project/yfinance/
- **Community Forum:** https://discuss.streamlit.io

---

## 📋 Pre-Deployment Checklist

- [ ] All dependencies in `requirements.txt`
- [ ] Disclaimer prominently displayed
- [ ] Error handling for invalid tickers
- [ ] Loading states for long operations
- [ ] Mobile-responsive design (Streamlit default)
- [ ] Clear "Educational Only" warnings
- [ ] Test with multiple tickers (AAPL, TSLA, NVDA)
- [ ] Test different timeframes and risk tolerances
- [ ] Code is clean and commented
- [ ] README is complete

---

## 🎉 You're Ready!

Your Stock Analysis app is production-ready and can be deployed to Streamlit Cloud in minutes!

**Next Steps:**
1. Test locally: `streamlit run app.py`
2. Push to GitHub
3. Deploy on Streamlit Cloud
4. Share with the world! 🚀

**Remember:** This is an educational tool. Always include proper disclaimers and encourage users to do their own research!
