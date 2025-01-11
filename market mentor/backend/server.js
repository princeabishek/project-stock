const express = require('express');
const path = require('path');
const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware for logging and debugging
app.use((req, res, next) => {
    console.log(`${req.method} request to ${req.path}`);
    next();
});

// Middleware
app.use(cors());
app.use(express.json());

// Serve static files
app.use(express.static(path.join(__dirname, '..', 'static')));

// Serve HTML templates
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, '..', 'templates', 'chatbot.html'));
});

// Detailed Query Route
app.post('/api/query', (req, res) => {
    try {
        const { query } = req.body;
        
        // Validate input
        if (!query) {
            return res.status(400).json({ 
                error: 'Query is required',
                details: 'Please provide a non-empty query'
            });
        }

        // Detailed response logic
        const processQuery = (userQuery) => {
            const lowerQuery = userQuery.toLowerCase();
            
            const responses = [
                { 
                    keywords: ['stock', 'apple', 'aapl'],
                    response: "Apple (AAPL) is a leading technology company known for innovative products like iPhone and Mac."
                },
                { 
                    keywords: ['google', 'alphabet', 'googl'],
                    response: "Alphabet (GOOGL) is the parent company of Google, focusing on internet services and technologies."
                },
                { 
                    keywords: ['help', 'info', 'about'],
                    response: "Market Mentor helps you get quick insights about stocks and companies. Ask about specific stocks or general market information."
                }
            ];

            // Find matching response
            const matchedResponse = responses.find(item => 
                item.keywords.some(keyword => lowerQuery.includes(keyword))
            );

            return matchedResponse 
                ? matchedResponse.response 
                : "I'm not sure about that. Try asking about specific stocks like Apple or Google.";
        };

        const response = processQuery(query);
        
        res.json({ 
            response,
            success: true 
        });

    } catch (error) {
        console.error('Query processing error:', error);
        res.status(500).json({ 
            error: 'Internal server error',
            details: error.message,
            success: false
        });
    }
});

// Error handling middleware
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ 
        error: 'Something broke!',
        details: err.message 
    });
});

// Start Server
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});