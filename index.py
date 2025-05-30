import requests
import time


def get_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 10,
        "page": 1,
        "sparkline": False
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch data.")
        return []


def chatbot_response(user_input, data):
    user_input = user_input.lower()

     # Greetings and help responses first
    if user_input in ["hi", "hello", "hey"]:
        return "Hey there! 👋 Ask me about crypto trends, sustainability, or long-term growth!"
    elif user_input == "help":
        return (
            "You can ask me things like:\n"
            "- Which crypto is trending?\n"
            "- What’s the most sustainable coin?\n"
            "- Suggestions for long-term profitable coins\n"
            "- Or just say 'bye' to exit."
        )
    # Crypto-related queries

    if "sustainable" in user_input or "eco" in user_input:
        
        sustainable = sorted(data, key=lambda x: x["total_volume"])
        coin = sustainable[0]
        return f"{coin['name']} ♻️ might be more eco-conscious (low activity). Do your research! ⚠️"

    elif "trending" in user_input or "rising" in user_input:
        trending = sorted(data, key=lambda x: x["price_change_percentage_24h"] or 0, reverse=True)
        coin = trending[0]
        return f"{coin['name']} 🚀 is trending up with a {coin['price_change_percentage_24h']:.2f}% increase today!"

    elif "long-term" in user_input or "profitable" in user_input:
        rising_high_cap = [
            coin for coin in data if (coin["price_change_percentage_24h"] or 0) > 0 and coin["market_cap_rank"] <= 3
        ]
        if rising_high_cap:
            coin = rising_high_cap[0]
            return f"For long-term growth, consider {coin['name']} 💰. Strong trend + high market cap!"
        else:
            return "No strong performers in the top ranks right now. Check back later! 📉"

    elif "bye" in user_input or "exit" in user_input:
        return "Goodbye! 👋 Stay safe and invest smart! ⚠️"

    else:
        return "Hmm... I didn’t get that 🤖. Ask me about trending, sustainability, or long-term growth!"


def run_chatbot():
    print("👋 Hello! I’m CryptoBuddy. Ask me about crypto trends, sustainability, or profitability!")
    data = get_crypto_data()
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["bye", "exit", "quit"]:
            print("CryptoBuddy:", chatbot_response(user_input, data))
            break
        response = chatbot_response(user_input, data)
        print("CryptoBuddy:", response)


run_chatbot()

