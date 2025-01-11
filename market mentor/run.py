import yfinance as yf
from django.shortcuts import render
from django.http import JsonResponse

def get_stock_data(symbol):
    # Fetch stock data using yfinance
    stock = yf.Ticker(symbol)
    hist = stock.history(period="1d")  # Get today's data for the stock
    current_price = hist["Close"].iloc[-1]  # Latest closing price
    yesterday_price = hist["Close"].iloc[-2]  # Previous day's closing price
    weekly_high = hist["High"].max()  # Weekly highest price
    weekly_high_day = hist["High"].idxmax()  # Day of the weekly high
    weekly_high_day_name = weekly_high_day.strftime('%A')  # Day of the week

    return {
        'current_price': current_price,
        'yesterday_price': yesterday_price,
        'weekly_high': weekly_high,
        'weekly_high_day': weekly_high_day.strftime('%Y-%m-%d'),
        'weekly_high_day_name': weekly_high_day_name
    }

def live_stocks(request):
    stocks = ['AAPL', 'GOOG', 'MSFT', 'AMZN', 'TSLA', 'NFLX', 'FB', 'NVDA', 'INTC', 'PYPL']
    stock_data = {}
    
    # Fetch data for each stock
    for stock in stocks:
        stock_data[stock] = get_stock_data(stock)
    
    return render(request, 'live_stocks.html', {'stock_data': stock_data})

def live_stocks_api(request):
    stocks = ['AAPL', 'GOOG', 'MSFT', 'AMZN', 'TSLA', 'NFLX', 'FB', 'NVDA', 'INTC', 'PYPL']
    stock_data = {}
    
    # Fetch live data for each stock
    for stock in stocks:
        stock_data[stock] = get_stock_data(stock)
    
    return JsonResponse(stock_data)
