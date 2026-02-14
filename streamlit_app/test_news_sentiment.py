"""
Test script for News & Sentiment Analysis
Tests with AAPL and TSLA as specified
"""
from news_sentiment import NewsSentimentAnalyzer


def test_ticker(ticker: str):
    """Test news sentiment for a ticker."""
    print(f"\n{'='*60}")
    print(f"Testing {ticker}")
    print(f"{'='*60}\n")
    
    analyzer = NewsSentimentAnalyzer(ticker)
    news_data = analyzer.get_news_with_sentiment(limit=5)
    
    if 'error' in news_data:
        print(f"❌ Error: {news_data['error']}")
        return False
    
    # Print overall sentiment
    overall = news_data['overall_sentiment']
    print(f"📊 Overall Sentiment: {overall['emoji']} {overall['sentiment']}")
    print(f"   Score: {overall['compound']:.3f}")
    print(f"   Articles: {overall['total_count']} total")
    print(f"   - 🟢 Positive: {overall['positive_count']} ({overall['positive_count']/overall['total_count']*100:.1f}%)")
    print(f"   - 🟡 Neutral: {overall['neutral_count']} ({overall['neutral_count']/overall['total_count']*100:.1f}%)")
    print(f"   - 🔴 Negative: {overall['negative_count']} ({overall['negative_count']/overall['total_count']*100:.1f}%)")
    
    # Print individual articles
    print(f"\n📰 Recent Articles:\n")
    for i, article in enumerate(news_data['articles'], 1):
        sentiment = article['sentiment']
        print(f"{i}. {sentiment['emoji']} {article['title']}")
        print(f"   Publisher: {article['publisher']}")
        print(f"   Published: {article['published_str']}")
        print(f"   Sentiment: {sentiment['sentiment']} (Score: {sentiment['compound']:.3f})")
        print(f"   Link: {article['link'][:80]}..." if len(article['link']) > 80 else f"   Link: {article['link']}")
        print()
    
    return True


if __name__ == "__main__":
    print("Testing News & Sentiment Analysis Feature")
    print("=" * 60)
    
    # Test AAPL
    success_aapl = test_ticker("AAPL")
    
    # Test TSLA
    success_tsla = test_ticker("TSLA")
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary:")
    print(f"  AAPL: {'✅ PASS' if success_aapl else '❌ FAIL'}")
    print(f"  TSLA: {'✅ PASS' if success_tsla else '❌ FAIL'}")
    print("=" * 60)
