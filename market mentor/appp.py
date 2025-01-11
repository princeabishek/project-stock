from flask import Flask, render_template
import requests
from textblob import TextBlob

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stock_trends')
def stock_trends():
    api_key = '2ed48bbeb7d8421088a491d32e804768'  # Replace with a valid NewsAPI key
    url = f'https://newsapi.org/v2/everything?q=stock market&sortBy=publishedAt&apiKey={api_key}'

    response = requests.get(url)
    if response.status_code != 200:
        return f"Error fetching news: {response.status_code}", 500

    articles = response.json().get('articles', [])
    trends = []
    for article in articles[:10]:  # Fetch top 10 articles
        sentiment = TextBlob(article['title']).sentiment.polarity
        trends.append({
            'title': article['title'],
            'url': article['url'],
            'sentiment': 'Positive' if sentiment > 0 else 'Negative' if sentiment < 0 else 'Neutral'
        })

    return render_template('stock_trends.html', trends=trends)

if __name__ == '__main__':
    app.run(debug=True)
