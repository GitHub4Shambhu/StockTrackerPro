import os
from newsapi import NewsApiClient
from textblob import TextBlob
import pandas as pd

def get_news_sentiment(symbol):
    try:
        # Initialize NewsApiClient with your API key
        newsapi = NewsApiClient(api_key=os.environ.get('NEWS_API_KEY'))

        # Fetch news articles
        articles = newsapi.get_everything(q=symbol, language='en', sort_by='publishedAt', page_size=10)

        # Perform sentiment analysis
        sentiments = []
        for article in articles['articles']:
            title = article['title']
            description = article['description'] or ''
            content = article['content'] or ''
            full_text = f"{title} {description} {content}"
            
            blob = TextBlob(full_text)
            sentiment = blob.sentiment.polarity
            
            sentiments.append({
                'title': title,
                'url': article['url'],
                'publishedAt': article['publishedAt'],
                'sentiment': sentiment
            })

        # Create a DataFrame with the results
        df = pd.DataFrame(sentiments)
        df['sentiment_category'] = pd.cut(df['sentiment'], 
                                          bins=[-1, -0.1, 0.1, 1], 
                                          labels=['Negative', 'Neutral', 'Positive'])
        
        return df
    except Exception as e:
        print(f"Error fetching news sentiment: {e}")
        return None
