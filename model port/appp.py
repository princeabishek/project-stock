# market_mentor.py
from flask import Flask, render_template, request, jsonify, session
import yfinance as yf
import random
import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a real secret key

class PortfolioManager:
    def __init__(self, initial_cash=100000):
        self.stocks = [
            'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 
            'ITC.NS', 'WIPRO.NS', 'BHARTIARTL.NS', 'LT.NS', 
            'HCLTECH.NS', 'TATAMOTORS.NS'
        ]
        self.stock_names = {
            'RELIANCE.NS': 'Reliance',
            'TCS.NS': 'TCS',
            'HDFCBANK.NS': 'HDFC Bank',
            'INFY.NS': 'Infosys',
            'ITC.NS': 'ITC',
            'WIPRO.NS': 'Wipro',
            'BHARTIARTL.NS': 'Airtel',
            'LT.NS': 'L&T',
            'HCLTECH.NS': 'HCL Tech',
            'TATAMOTORS.NS': 'Tata Motors'
        }
        self.initial_cash = initial_cash

    def get_current_prices(self):
        prices = {}
        for stock in self.stocks:
            try:
                ticker = yf.Ticker(stock)
                current_price = ticker.history(period='1d')['Close'][-1]
                prices[stock] = round(current_price, 2)
            except Exception as e:
                prices[stock] = random.uniform(100, 1000)  # Fallback random price
        return prices

    def simulate_price_change(self, current_prices):
        changed_prices = {}
        for stock, price in current_prices.items():
            # Simulate price change between -5% to +5%
            change_percent = random.uniform(-0.05, 0.05)
            new_price = price * (1 + change_percent)
            changed_prices[stock] = round(new_price, 2)
        return changed_prices

# Routes
@app.route('/')
def home():
    portfolio_manager = PortfolioManager()
    current_prices = portfolio_manager.get_current_prices()
    
    # Initialize session variables if not exists
    if 'portfolio' not in session:
        session['portfolio'] = {stock: 0 for stock in portfolio_manager.stocks}
    if 'cash' not in session:
        session['cash'] = portfolio_manager.initial_cash

    return render_template('index.html', 
                           stocks=portfolio_manager.stock_names, 
                           prices=current_prices,
                           cash=session['cash'],
                           portfolio=session['portfolio'])

@app.route('/buy', methods=['POST'])
def buy_stock():
    portfolio_manager = PortfolioManager()
    stock = request.form.get('stock')
    quantity = int(request.form.get('quantity', 0))
    
    current_prices = portfolio_manager.get_current_prices()
    total_cost = current_prices[stock] * quantity

    if total_cost <= session['cash']:
        session['cash'] -= total_cost
        session['portfolio'][stock] += quantity
        session.modified = True
        return jsonify({
            'success': True, 
            'cash': session['cash'], 
            'portfolio': session['portfolio']
        })
    
    return jsonify({'success': False, 'message': 'Insufficient funds'})

@app.route('/sell', methods=['POST'])
def sell_stock():
    portfolio_manager = PortfolioManager()
    stock = request.form.get('stock')
    quantity = int(request.form.get('quantity', 0))
    
    current_prices = portfolio_manager.get_current_prices()
    total_sale = current_prices[stock] * quantity

    if session['portfolio'][stock] >= quantity:
        session['cash'] += total_sale
        session['portfolio'][stock] -= quantity
        session.modified = True
        return jsonify({
            'success': True, 
            'cash': session['cash'], 
            'portfolio': session['portfolio']
        })
    
    return jsonify({'success': False, 'message': 'Insufficient stocks'})

@app.route('/simulate_time', methods=['POST'])
def simulate_time():
    portfolio_manager = PortfolioManager()
    current_prices = portfolio_manager.get_current_prices()
    new_prices = portfolio_manager.simulate_price_change(current_prices)
    
    return jsonify({
        'old_prices': current_prices,
        'new_prices': new_prices
    })

if __name__ == '__main__':
    app.run(debug=True)