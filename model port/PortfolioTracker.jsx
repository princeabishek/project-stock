import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { PlusCircle, MinusCircle, TrendingUp } from 'lucide-react';

const PortfolioTracker = () => {
  const [portfolio, setPortfolio] = useState({
    initialCash: 100000,
    availableCash: 100000,
    totalValue: 100000,
    profitLoss: 0,
    holdings: []
  });

  const [stocks, setStocks] = useState([
    { symbol: 'RELIANCE', price: 2500, prevPrice: 2500, change: 0 },
    { symbol: 'TCS', price: 3200, prevPrice: 3200, change: 0 },
    { symbol: 'HDFC', price: 1400, prevPrice: 1400, change: 0 },
    { symbol: 'INFY', price: 1300, prevPrice: 1300, change: 0 },
    { symbol: 'ITC', price: 250, prevPrice: 250, change: 0 },
    { symbol: 'WIPRO', price: 400, prevPrice: 400, change: 0 },
    { symbol: 'AIRTEL', price: 700, prevPrice: 700, change: 0 },
    { symbol: 'LT', price: 2000, prevPrice: 2000, change: 0 },
    { symbol: 'HCLTECH', price: 1100, prevPrice: 1100, change: 0 },
    { symbol: 'TATAMOTORS', price: 600, prevPrice: 600, change: 0 }
  ]);

  const [selectedQuantity, setSelectedQuantity] = useState(1);
  const [elapsedMinutes, setElapsedMinutes] = useState(0);

  useEffect(() => {
    const updatePrices = () => {
      setStocks(prevStocks => {
        return prevStocks.map(stock => {
          const volatility = (Math.random() - 0.5) * 0.02; // 2% max movement
          const newPrice = Math.max(stock.price * (1 + volatility), 0.01);
          return {
            ...stock,
            prevPrice: stock.price,
            price: parseFloat(newPrice.toFixed(2)),
            change: parseFloat(((newPrice - stock.price) / stock.price * 100).toFixed(2))
          };
        });
      });

      // Update portfolio value
      setPortfolio(prev => {
        const holdingsValue = prev.holdings.reduce((total, holding) => {
          const currentStock = stocks.find(s => s.symbol === holding.symbol);
          return total + (currentStock ? currentStock.price * holding.quantity : 0);
        }, 0);

        const newTotalValue = holdingsValue + prev.availableCash;
        const newProfitLoss = newTotalValue - prev.initialCash;

        return {
          ...prev,
          totalValue: parseFloat(newTotalValue.toFixed(2)),
          profitLoss: parseFloat(newProfitLoss.toFixed(2))
        };
      });

      setElapsedMinutes(prev => prev + 2);
    };

    const interval = setInterval(updatePrices, 2000); // Update every 2 seconds
    return () => clearInterval(interval);
  }, [stocks]);

  const buyStock = (stock) => {
    const totalCost = stock.price * selectedQuantity;
    
    if (totalCost > portfolio.availableCash) {
      alert('Insufficient funds!');
      return;
    }

    setPortfolio(prev => {
      const existingHolding = prev.holdings.find(h => h.symbol === stock.symbol);
      let newHoldings;

      if (existingHolding) {
        newHoldings = prev.holdings.map(h => 
          h.symbol === stock.symbol 
            ? {
                ...h,
                quantity: h.quantity + selectedQuantity,
                avgPrice: ((h.avgPrice * h.quantity) + (stock.price * selectedQuantity)) / (h.quantity + selectedQuantity)
              }
            : h
        );
      } else {
        newHoldings = [...prev.holdings, {
          symbol: stock.symbol,
          quantity: selectedQuantity,
          avgPrice: stock.price,
        }];
      }

      return {
        ...prev,
        availableCash: prev.availableCash - totalCost,
        holdings: newHoldings
      };
    });
  };

  const sellStock = (stock) => {
    const holding = portfolio.holdings.find(h => h.symbol === stock.symbol);
    
    if (!holding || holding.quantity < selectedQuantity) {
      alert('Insufficient stocks to sell!');
      return;
    }

    const saleValue = stock.price * selectedQuantity;

    setPortfolio(prev => {
      const newHoldings = prev.holdings
        .map(h => {
          if (h.symbol === stock.symbol) {
            const newQuantity = h.quantity - selectedQuantity;
            return newQuantity > 0 
              ? { ...h, quantity: newQuantity }
              : null;
          }
          return h;
        })
        .filter(Boolean);

      return {
        ...prev,
        availableCash: prev.availableCash + saleValue,
        holdings: newHoldings
      };
    });
  };

  return (
    <div className="p-4 bg-gray-50 min-h-screen">
      {/* Portfolio Summary */}
      <div className="bg-white rounded-lg shadow p-4 mb-4">
        <h1 className="text-2xl font-bold mb-4">My Portfolio</h1>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="p-3 bg-gray-50 rounded-lg">
            <p className="text-gray-600">Available Cash</p>
            <p className="text-xl font-bold">₹{portfolio.availableCash.toLocaleString()}</p>
          </div>
          <div className="p-3 bg-gray-50 rounded-lg">
            <p className="text-gray-600">Total Value</p>
            <p className="text-xl font-bold">₹{portfolio.totalValue.toLocaleString()}</p>
          </div>
          <div className="p-3 bg-gray-50 rounded-lg">
            <p className="text-gray-600">P&L</p>
            <p className={`text-xl font-bold ${portfolio.profitLoss >= 0 ? 'text-green-600' : 'text-red-600'}`}>
              ₹{portfolio.profitLoss.toLocaleString()}
            </p>
          </div>
          <div className="p-3 bg-gray-50 rounded-lg">
            <p className="text-gray-600">Time Elapsed</p>
            <p className="text-xl font-bold">{elapsedMinutes} min</p>
          </div>
        </div>
      </div>

      {/* Holdings */}
      {portfolio.holdings.length > 0 && (
        <div className="bg-white rounded-lg shadow p-4 mb-4">
          <h2 className="text-xl font-bold mb-3">Current Holdings</h2>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="text-left border-b">
                  <th className="p-2">Stock</th>
                  <th className="p-2">Quantity</th>
                  <th className="p-2">Avg Price</th>
                  <th className="p-2">Current Price</th>
                  <th className="p-2">P&L</th>
                </tr>
              </thead>
              <tbody>
                {portfolio.holdings.map(holding => {
                  const currentStock = stocks.find(s => s.symbol === holding.symbol);
                  const profitLoss = (currentStock.price - holding.avgPrice) * holding.quantity;
                  return (
                    <tr key={holding.symbol} className="border-b">
                      <td className="p-2">{holding.symbol}</td>
                      <td className="p-2">{holding.quantity}</td>
                      <td className="p-2">₹{holding.avgPrice.toFixed(2)}</td>
                      <td className="p-2">₹{currentStock.price.toFixed(2)}</td>
                      <td className={`p-2 ${profitLoss >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                        ₹{profitLoss.toFixed(2)}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Stock List */}
      <div className="bg-white rounded-lg shadow p-4">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-bold">Available Stocks</h2>
          <div className="flex items-center space-x-2">
            <label className="text-sm text-gray-600">Quantity:</label>
            <input
              type="number"
              min="1"
              value={selectedQuantity}
              onChange={(e) => setSelectedQuantity(Math.max(1, parseInt(e.target.value) || 1))}
              className="w-20 p-1 border rounded"
            />
          </div>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {stocks.map(stock => (
            <div key={stock.symbol} className="border rounded-lg p-4">
              <div className="flex justify-between items-start mb-2">
                <div>
                  <h3 className="font-bold">{stock.symbol}</h3>
                  <p className="text-xl">₹{stock.price.toFixed(2)}</p>
                </div>
                <div className={`px-2 py-1 rounded ${stock.change >= 0 ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                  {stock.change >= 0 ? '+' : ''}{stock.change}%
                </div>
              </div>
              <div className="flex space-x-2 mt-4">
                <button
                  onClick={() => buyStock(stock)}
                  className="flex-1 bg-green-500 text-white py-2 px-4 rounded hover:bg-green-600 flex items-center justify-center space-x-1"
                >
                  <PlusCircle size={16} />
                  <span>Buy</span>
                </button>
                <button
                  onClick={() => sellStock(stock)}
                  className="flex-1 bg-red-500 text-white py-2 px-4 rounded hover:bg-red-600 flex items-center justify-center space-x-1"
                >
                  <MinusCircle size={16} />
                  <span>Sell</span>
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default PortfolioTracker;