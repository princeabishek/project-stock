// Initialize the charts
const liveStockCtx = document.getElementById('liveStockChart').getContext('2d');
const portfolioCtx = document.getElementById('portfolioChart').getContext('2d');
const marketTrendCtx = document.getElementById('marketTrendChart').getContext('2d');

// Live Stock Prices Chart
const liveStockChart = new Chart(liveStockCtx, {
    type: 'line',
    data: {
        labels: ['AAPL', 'GOOG', 'AMZN', 'TSLA', 'MSFT'],
        datasets: [{
            label: 'Stock Price',
            data: [150, 180, 170, 250, 300],
            backgroundColor: 'rgba(21, 101, 192, 0.2)',
            borderColor: '#1565c0',
            borderWidth: 2
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: { beginAtZero: false }
        }
    }
});

// Model Portfolio Chart
const portfolioChart = new Chart(portfolioCtx, {
    type: 'pie',
    data: {
        labels: ['Stocks', 'Bonds', 'Real Estate', 'Cash'],
        datasets: [{
            data: [45, 25, 15, 15],
            backgroundColor: ['#ff6384', '#36a2eb', '#ffcd56', '#4bc0c0']
        }]
    },
    options: {
        responsive: true
    }
});

// Market Trends Chart
const marketTrendChart = new Chart(marketTrendCtx, {
    type: 'bar',
    data: {
        labels: ['Tech', 'Healthcare', 'Finance', 'Energy', 'Utilities'],
        datasets: [{
            label: 'Market Growth (%)',
            data: [5, 3, 4, 6, 2],
            backgroundColor: '#42a5f5',
            borderColor: '#1e88e5',
            borderWidth: 1
        }]
    },
    options: {
        responsive: true
    }
});
