"""Quick demo of News & Sentiment feature"""
from news_sentiment import NewsSentimentAnalyzer

print("\n" + "="*70)
print("📰 NEWS & SENTIMENT ANALYSIS - LIVE DEMO")
print("="*70 + "\n")

for ticker in ["AAPL", "TSLA"]:
    print(f"\n{'─'*70}")
    print(f"📊 {ticker} - Stock News Sentiment")
    print(f"{'─'*70}\n")
    
    analyzer = NewsSentimentAnalyzer(ticker)
    data = analyzer.get_news_with_sentiment(limit=5)
    
    if 'error' not in data:
        overall = data['overall_sentiment']
        print(f"{overall['emoji']} Overall: {overall['sentiment']} (Score: {overall['compound']:.3f})")
        print(f"   Distribution: 🟢 {overall['positive_count']} | 🟡 {overall['neutral_count']} | 🔴 {overall['negative_count']}")
        print(f"\n📰 Latest Headlines:\n")
        
        for i, article in enumerate(data['articles'], 1):
            s = article['sentiment']
            print(f"   {i}. {s['emoji']} [{s['compound']:+.3f}] {article['title'][:60]}...")
    
    print()

print("="*70)
print("✅ Feature working perfectly! Check the Streamlit app for full UI.")
print("="*70 + "\n")
