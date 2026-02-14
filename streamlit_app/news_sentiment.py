"""
News & Sentiment Analysis Module
Fetches news from yfinance and analyzes sentiment using VADER
"""
import yfinance as yf
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime
from typing import List, Dict, Optional


class NewsSentimentAnalyzer:
    """Fetch and analyze news sentiment for stocks."""
    
    def __init__(self, ticker: str):
        """
        Initialize analyzer.
        
        Args:
            ticker: Stock ticker symbol
        """
        self.ticker = ticker
        self.analyzer = SentimentIntensityAnalyzer()
    
    def fetch_news(self, limit: int = 10) -> List[Dict]:
        """
        Fetch recent news articles.
        
        Args:
            limit: Maximum number of articles to fetch
            
        Returns:
            List of news articles with metadata
        """
        try:
            stock = yf.Ticker(self.ticker)
            news = stock.news
            
            if not news:
                return []
            
            # Limit to requested number of articles
            news = news[:limit]
            
            # Format news data
            formatted_news = []
            for article in news:
                # Handle nested content structure
                content = article.get('content', {})
                
                # Extract title and other fields
                title = content.get('title', article.get('title', 'No title'))
                publisher = content.get('provider', {}).get('displayName', article.get('publisher', 'Unknown'))
                
                # Get URL from canonicalUrl or clickThroughUrl
                link = ''
                if 'canonicalUrl' in content:
                    link = content['canonicalUrl'].get('url', '')
                elif 'clickThroughUrl' in content:
                    link = content['clickThroughUrl'].get('url', '')
                elif 'link' in article:
                    link = article['link']
                
                # Get publication date
                pub_date = None
                pub_date_str = 'Unknown date'
                
                if 'pubDate' in content:
                    try:
                        # Parse ISO format date
                        from dateutil import parser
                        pub_date = parser.parse(content['pubDate'])
                        pub_date_str = pub_date.strftime('%Y-%m-%d %H:%M')
                    except:
                        pub_date_str = content['pubDate'][:16].replace('T', ' ')
                elif 'displayTime' in content:
                    try:
                        from dateutil import parser
                        pub_date = parser.parse(content['displayTime'])
                        pub_date_str = pub_date.strftime('%Y-%m-%d %H:%M')
                    except:
                        pub_date_str = content['displayTime'][:16].replace('T', ' ')
                elif 'providerPublishTime' in article:
                    try:
                        pub_date = datetime.fromtimestamp(article['providerPublishTime'])
                        pub_date_str = pub_date.strftime('%Y-%m-%d %H:%M')
                    except:
                        pass
                
                # Get thumbnail
                thumbnail = ''
                if 'thumbnail' in content and content['thumbnail']:
                    resolutions = content['thumbnail'].get('resolutions', [])
                    if resolutions:
                        # Get smallest resolution for preview
                        thumbnail = resolutions[-1].get('url', '')
                
                formatted_article = {
                    'title': title,
                    'publisher': publisher,
                    'link': link,
                    'published_str': pub_date_str,
                    'thumbnail': thumbnail,
                    'summary': content.get('summary', content.get('description', ''))
                }
                
                formatted_news.append(formatted_article)
            
            return formatted_news
            
        except Exception as e:
            print(f"Error fetching news: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def analyze_sentiment(self, text: str) -> Dict:
        """
        Analyze sentiment of text using VADER.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with sentiment scores
        """
        scores = self.analyzer.polarity_scores(text)
        
        # Determine overall sentiment
        compound = scores['compound']
        if compound >= 0.05:
            sentiment = 'Positive'
            emoji = '🟢'
        elif compound <= -0.05:
            sentiment = 'Negative'
            emoji = '🔴'
        else:
            sentiment = 'Neutral'
            emoji = '🟡'
        
        return {
            'compound': compound,
            'positive': scores['pos'],
            'neutral': scores['neu'],
            'negative': scores['neg'],
            'sentiment': sentiment,
            'emoji': emoji
        }
    
    def get_news_with_sentiment(self, limit: int = 10) -> Dict:
        """
        Fetch news and analyze sentiment for each article.
        
        Args:
            limit: Maximum number of articles
            
        Returns:
            Dictionary with articles and overall sentiment
        """
        news_articles = self.fetch_news(limit)
        
        if not news_articles:
            return {
                'articles': [],
                'overall_sentiment': {
                    'compound': 0.0,
                    'sentiment': 'Neutral',
                    'emoji': '🟡',
                    'positive_count': 0,
                    'neutral_count': 0,
                    'negative_count': 0
                },
                'error': 'No news articles found'
            }
        
        # Analyze sentiment for each article
        for article in news_articles:
            article['sentiment'] = self.analyze_sentiment(article['title'])
        
        # Calculate overall sentiment
        overall_compound = sum(a['sentiment']['compound'] for a in news_articles) / len(news_articles)
        
        # Count sentiment types
        positive_count = sum(1 for a in news_articles if a['sentiment']['sentiment'] == 'Positive')
        neutral_count = sum(1 for a in news_articles if a['sentiment']['sentiment'] == 'Neutral')
        negative_count = sum(1 for a in news_articles if a['sentiment']['sentiment'] == 'Negative')
        
        # Determine overall sentiment
        if overall_compound >= 0.05:
            overall_sentiment_label = 'Positive'
            overall_emoji = '🟢'
        elif overall_compound <= -0.05:
            overall_sentiment_label = 'Negative'
            overall_emoji = '🔴'
        else:
            overall_sentiment_label = 'Neutral'
            overall_emoji = '🟡'
        
        return {
            'articles': news_articles,
            'overall_sentiment': {
                'compound': overall_compound,
                'sentiment': overall_sentiment_label,
                'emoji': overall_emoji,
                'positive_count': positive_count,
                'neutral_count': neutral_count,
                'negative_count': negative_count,
                'total_count': len(news_articles)
            }
        }
    
    def get_sentiment_summary(self, news_data: Dict) -> str:
        """
        Generate human-readable sentiment summary.
        
        Args:
            news_data: News data from get_news_with_sentiment()
            
        Returns:
            Summary string
        """
        if 'error' in news_data:
            return "No recent news found for this ticker."
        
        overall = news_data['overall_sentiment']
        total = overall['total_count']
        pos = overall['positive_count']
        neu = overall['neutral_count']
        neg = overall['negative_count']
        
        summary = f"{overall['emoji']} **Overall Sentiment: {overall['sentiment']}** (Score: {overall['compound']:.3f})\n\n"
        summary += f"Analyzed {total} recent articles:\n"
        summary += f"- 🟢 {pos} Positive ({pos/total*100:.1f}%)\n"
        summary += f"- 🟡 {neu} Neutral ({neu/total*100:.1f}%)\n"
        summary += f"- 🔴 {neg} Negative ({neg/total*100:.1f}%)\n"
        
        return summary
