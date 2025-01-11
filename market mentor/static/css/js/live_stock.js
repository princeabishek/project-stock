// script.js
const companies = [
    "Company A",
    "Company B",
    // ...
];

function fetchAndDisplayData() {
    companies.forEach(company => {
        fetch(`https://api.example.com/stock-price/${company}`)
            .then(response => response.json())
            .then(data => {
                document.getElementById(`current-price-${company}`).textContent = data.currentPrice;
                document.getElementById(`yesterday-price-${company}`).textContent = data.yesterdayPrice;
                document.getElementById(`week-high-${company}`).textContent = data.weekHigh;
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
    });
}

setInterval(fetchAndDisplayData, 60000); // Update every minute