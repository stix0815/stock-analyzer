"""Debug script to check yfinance news structure"""
import yfinance as yf
import json

ticker = yf.Ticker("AAPL")
news = ticker.news

print(f"Found {len(news)} news items")
print("\nFirst article structure:")
print(json.dumps(news[0] if news else {}, indent=2, default=str))
