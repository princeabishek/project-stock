// Portfolio Chart
var ctx = document.getElementById('portfolioChart').getContext('2d');
var portfolioChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['January', 'February', 'March', 'April', 'May'],
        datasets: [{
            label: 'Portfolio Value',
            data: [1000, 1500, 2000, 2500, 3000],
            borderColor: '#28a745',
            fill: false
        }]
    },
    options: {
        responsive: true
    }
});

// Market Trends Chart
var ctx2 = document.getElementById('marketTrendChart').getContext('2d');
var marketTrendChart = new Chart(ctx2, {
    type: 'bar',
    data: {
        labels: ['Tech', 'Finance', 'Energy', 'Healthcare', 'Consumer'],
        datasets: [{
            label: 'Stock Trends',
            data: [50, 30, 40, 60, 80],
            backgroundColor: ['#003366', '#28a745', '#f39c12', '#e74c3c', '#8e44ad']
        }]
    },
    options: {
        responsive: true
    }
});
async function sendToChatbot() {
    const userMessage = document.getElementById("chat-input").value;
    const response = await fetch('http://localhost:3001/api/query', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: message }),
    });
    const data = await response.json();
    displayChatbotResponse(data.response);
}

function displayChatbotResponse(message) {
    const chatContainer = document.getElementById("chat-container");
    const chatbotMessage = document.createElement("div");
    chatbotMessage.classList.add("chatbot-response");
    chatbotMessage.textContent = message;
    chatContainer.appendChild(chatbotMessage);
}


// Chatbot Popup (Just an example)
document.getElementById('chatbot-btn').addEventListener('click', function() {
    alert("Chatbot coming soon!");
});
