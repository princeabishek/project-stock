import os
from dotenv import load_dotenv
import json
import gradio as gr
import requests
import time

load_dotenv()

# Configuration
news_api_key = os.getenv("ALPHAVANTAGE_API_KEY")
if not news_api_key:
     news_api_key = "YOUR_ALPHAVANTAGE_API_KEY"
if news_api_key =="YOUR_ALPHAVANTAGE_API_KEY":
      raise ValueError("ALPHAVANTAGE_API_KEY not found. Please set the API_KEY environment variable or update the code to include it")

data_api_key = os.getenv("ALPHAVANTAGE_API_KEY")
if not data_api_key:
    data_api_key = "YOUR_ALPHAVANTAGE_API_KEY"
if data_api_key =="YOUR_ALPHAVANTAGE_API_KEY":
      raise ValueError("ALPHAVANTAGE_API_KEY not found. Please set the API_KEY environment variable or update the code to include it")
# News Section
def get_stock_news(api_key, keywords="stock market"):
      url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers=AAPL,TSLA&apikey={api_key}"

      try:
          response = requests.get(url)
          response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
          data = response.json()

          news_items = []
          if 'feed' in data:
            for item in data['feed']:
                news_items.append({
                    'title': item.get('title', 'No Title'),
                    'summary': item.get('summary', 'No Summary'),
                     'url': item.get('url', '#'),
                     'time_published': item.get('time_published', 'Unknown Time')
                })
          return news_items
      except requests.exceptions.RequestException as e:
          print(f"Error fetching news: {e}")
          return []

def create_news_tab():
    def get_news():
        news_data = get_stock_news(news_api_key) # get the news data
        if news_data:
           news_display_text = ""
           for item in news_data:
                news_display_text += f"**Title:** {item['title']}<br>"
                news_display_text += f"**Summary:** {item['summary']}<br>"
                news_display_text += f"**URL:** <a href='{item['url']}'>{item['url']}</a><br>"
                news_display_text += f"**Published Time:** {item['time_published']}<br>"
                news_display_text += "<hr>"  # add a separator
           return news_display_text
        else:
           return "Error fetching news"
    with gr.Column():
      news_display = gr.Markdown("Fetching News...")
      news_button = gr.Button("Refresh News")

      news_button.click(get_news, outputs=[news_display])
    return news_display

# Trend Section
def get_historical_stock_data(api_key, ticker="AAPL"):
      url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&outputsize=full&apikey={api_key}"
      try:
          response = requests.get(url)
          response.raise_for_status()
          data = response.json()
          if "Time Series (Daily)" in data:
              time_series = data["Time Series (Daily)"]
              return time_series
          else:
            return None
      except requests.exceptions.RequestException as e:
           print(f"Error fetching historical data for {ticker}: {e}")
           return None

def calculate_stock_trends(api_key):
  tickers = ["AAPL", "GOOG", "TSLA", "MSFT", "AMZN", "NVDA"] # Add more here if you need
  yearly_data = {}
  all_data = {}
  for ticker in tickers:
       historical_data = get_historical_stock_data(api_key, ticker)
       if historical_data:
          dates = sorted(historical_data.keys())
          highest = 0
          lowest = 10000000
          first_date = None
          last_date = None
          last_price = None
          first_price = None
          for date in dates:
             high = float(historical_data[date]["2. high"])
             low = float(historical_data[date]["3. low"])
             if high > highest:
                highest = high
             if low < lowest:
                lowest = low
             if not first_date:
                 first_date = date
                 first_price = float(historical_data[date]["4. close"])
             last_date = date
             last_price = float(historical_data[date]["4. close"])
          yearly_data[ticker] = {"52_week_high":highest, "52_week_low":lowest}
          all_data[ticker] = { "first_date":first_date, "last_date":last_date, "last_price":last_price,"first_price":first_price}
  if all_data:
    risers = []
    fallers = []
    for ticker, data in all_data.items():
        change = data["last_price"] - data["first_price"]
        percent_change = (change / data["first_price"]) * 100
        all_data[ticker]["percent_change"] = percent_change
        if percent_change > 0:
            risers.append({"ticker":ticker, "percent_change":percent_change})
        else:
            fallers.append({"ticker":ticker,"percent_change":percent_change})
    risers = sorted(risers, key=lambda x: x["percent_change"], reverse=True)
    fallers = sorted(fallers, key=lambda x: x["percent_change"])
    top_risers = risers[:10]
    top_fallers = fallers[:10]
    top_gain = top_risers[0] if top_risers else None
    top_loss = top_fallers[0] if top_fallers else None
  else:
      top_risers = []
      top_fallers = []
      top_gain = None
      top_loss = None

  return yearly_data, top_risers, top_fallers, top_gain, top_loss


def create_trends_tab():
    def get_stock_trends():
        yearly_data, top_risers, top_fallers, top_gain, top_loss = calculate_stock_trends(data_api_key)

        if yearly_data:
          yearly_table = []
          for ticker, values in yearly_data.items():
                yearly_table.append({
                    "Ticker":ticker,
                    "52 Week High":values["52_week_high"],
                    "52 Week Low": values["52_week_low"]
                })
        else:
            yearly_table = []


        if top_risers:
            risers_table = []
            for item in top_risers:
                risers_table.append({"Ticker":item["ticker"], "Percentage Change":item["percent_change"]})
        else:
          risers_table = []

        if top_fallers:
            fallers_table = []
            for item in top_fallers:
               fallers_table.append({"Ticker": item["ticker"], "Percentage Change": item["percent_change"]})
        else:
          fallers_table = []

        gain_display_text = f"No Top Gain Available"
        if top_gain:
            gain_display_text = f"**Top Gaining Stock:** {top_gain['ticker']} <br>**Percent Change:** {top_gain['percent_change']:.2f}%"

        loss_display_text = f"No Top Loss Available"
        if top_loss:
            loss_display_text = f"**Top Losing Stock:** {top_loss['ticker']} <br>**Percent Change:** {top_loss['percent_change']:.2f}%"


        return  yearly_table, risers_table, fallers_table, gain_display_text, loss_display_text

    with gr.Column():
        yearly_display = gr.Dataframe()
        risers_display = gr.Dataframe()
        fallers_display = gr.Dataframe()
        gain_display = gr.Markdown()
        loss_display = gr.Markdown()
        trend_button = gr.Button("Refresh Stock Data")

        trend_button.click(get_stock_trends, outputs=[ yearly_display, risers_display, fallers_display, gain_display, loss_display])

        with gr.Row():
            with gr.Column():
                 gr.Markdown("Yearly Data")
                 yearly_display
            with gr.Column():
                gr.Markdown("Top Risers")
                risers_display
            with gr.Column():
               gr.Markdown("Top Fallers")
               fallers_display
        with gr.Row():
            with gr.Column():
                gr.Markdown("Top 1 Gain")
                gain_display
            with gr.Column():
                gr.Markdown("Top 1 Loss")
                loss_display

    return yearly_display, risers_display, fallers_display, gain_display, loss_display

with gr.Blocks(title="Market Mentor") as demo:
    gr.Markdown(
        """
        # Market Mentor
        ### Your Guide to the Stock Market
        ##### Get the latest trends
        """
        , elem_id="header-markdown"
    )
    with gr.Tab("Live News"):
      news_tab = create_news_tab()
    with gr.Tab("Stock Trends"):
       yearly_display, risers_display, fallers_display, gain_display, loss_display = create_trends_tab()

    css = """
      #header-markdown {
      text-align: center;
    }
      .gradio-container {
        background-color: #F5F5F5; /* Light Gray background for the app */
      }
      .gr-button {
        background-color: #1A237E; /* button background for the send and clear button */
        color: white;
        font-weight: bold;
      }
    """
    demo.load(None, inputs=None, outputs=None)
    demo.launch(share=False)