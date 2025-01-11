def get_chatbot_response(message):
    # Basic mock response - later, integrate with stock APIs or add logic
    if "price for" in message.lower():
        ticker = message.split("price for ")[1].strip().upper()
        return f"The price for {ticker} is currently unavailable (mock response)."
    else:
        return "I'm here to help with stock prices! Ask me about a specific stock ticker."
