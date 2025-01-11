import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
import gradio as gr

load_dotenv()

api_key = os.getenv("API_KEY")
if not api_key:
    api_key = "YOUR_GEMINI_API_KEY"
    if api_key == "YOUR_GEMINI_API_KEY":
        raise ValueError("API_KEY not found. Please set the API_KEY environment variable or update the code to include it")
genai.configure(api_key=api_key)

model = genai.GenerativeModel('gemini-pro')

try:
    with open('knowledge_base.json', 'r') as f:
        knowledge_base = json.load(f)
except FileNotFoundError:
    knowledge_base = {}
    print("Warning: knowledge_base.json not found. Starting with empty knowledge base.")

def get_response_from_knowledge_base(intent):
    """Retrieve pre-defined responses from the knowledge base if available."""
    if intent in knowledge_base:
        return knowledge_base[intent]
    return None

def is_stock_market_related(user_input):
    """
    Checks if the user's input is likely related to the stock market.
    """
    keywords = [
        "stock", "market", "invest", "share", "dividend", "ipo", "trading",
        "bonds", "portfolio", "analysis", "broker", "fund", "etf", "capital",
        "bull", "bear", "volume", "chart", "price"
    ]
    user_input_lower = user_input.lower()
    return any(keyword in user_input_lower for keyword in keywords)

def chat_with_gemini(user_input, chat_history):
        """
    Interacts with Gemini model using generate_content and maintains chat history.
    """
        prompt = f"""
            You are an expert stock market tutor named Sage whose job is to educate people on the stock market.
            If the user asks anything not stock market related politely decline.
            Otherwise answer the question and keep your answers concise, and precise.
            include stock market  prices live or current update in your response.
            """

        # Transform chat history into the format required by Gemini API
        gemini_formatted_history = []
        gemini_formatted_history.append({"role":"user", "parts":[prompt]}) #add prompt to the initial user message
        for turn in chat_history:
            gemini_formatted_history.append({"role": "user", "parts":[turn[0]]}) # previous user message
            gemini_formatted_history.append({"role":"model","parts":[turn[1]]}) #previous chatbot message

        gemini_formatted_history.append({"role":"user","parts":[user_input]}) #add the current user input to the end
        response = model.generate_content(gemini_formatted_history)
        return response.text


def chatbot(user_input, chat_history):
        if not user_input:
            return "Please ask a question", chat_history

        if is_stock_market_related(user_input):
            # Check if question is in knowledge base
            response_from_kb = get_response_from_knowledge_base(user_input)
            if response_from_kb:
                bot_response = response_from_kb
                chat_history.append((user_input, bot_response))
                return "", chat_history
            else:
                gemini_response = chat_with_gemini(user_input, chat_history)
                bot_response = gemini_response
                chat_history.append((user_input, bot_response))
                return "", chat_history
        else:
            bot_response = "I can only answer questions about the stock market."
            chat_history.append((user_input, bot_response))
            return "", chat_history

def clear_history():
    return []

with gr.Blocks(title="Market Mentor") as demo:
    gr.Markdown(
        """
        # Market Mentor
        ### Your Guide to the Stock Market
        ##### I am Sage, your stock market tutor
        """
        , elem_id="header-markdown"
    )

    with gr.Row():
        with gr.Column(scale=1):
          with gr.Accordion("Categories"):
              gr.Markdown(
               """
               ### Main
                * Basics
                * Investing
                * Analysis
                * Risk

               ### Topics
               * What are Stocks
               * How to Trade
               * What are IPO's
               * And many more!
              """,
              elem_id="category-markdown"
          )
        with gr.Column(scale=4):
            chatbot_state = gr.State([]) # State to store chatbot history
            chatbot_history = gr.Chatbot(elem_id="chat_bot")
            input_text = gr.Textbox(placeholder="Enter your question here...")

            with gr.Row():
              clear_btn = gr.Button("Clear History", variant="secondary")
              submit_btn = gr.Button("Send", variant="primary")

        clear_btn.click(clear_history, outputs=chatbot_state)


    submit_btn.click(chatbot,
                  [input_text, chatbot_state],
                  [input_text, chatbot_history])
    input_text.submit(chatbot,
                      [input_text, chatbot_state],
                      [input_text, chatbot_history])




    css = """
      #header-markdown {
      text-align: center;
    }

      #chat_bot {
      height: 400px; /* Set the desired height */
      overflow-y: auto;
      border: 1px solid #ccc;
      padding: 10px;
      }

      .gradio-container {
        background-color: #F5F5F5; /* Light Gray background for the app */
      }

      #chat_bot .user {
      background-color: #1A237E;
      color: white;
      align-items:flex-end;
      border-radius: 10px;
        padding: 8px;
      margin-bottom: 5px;
        }

      #chat_bot .bot {
      background-color: #4DD0E1; /* Teal background for bot messages */
        color: black;
          border-radius: 10px;
          padding: 8px;
      margin-bottom: 5px;
        }
     #category-markdown{
      padding-left: 10px;
    }
      .gr-button {
        background-color: #1A237E; /* button background for the send and clear button */
        color: white;
        font-weight: bold;
      }
    """

    demo.load(None,inputs=None, outputs=None)
    demo.launch(share=False)