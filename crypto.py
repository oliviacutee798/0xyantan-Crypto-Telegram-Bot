import os
import requests
from pyrogram import Client, filters

# Set up the Pyrogram client
api_id = os.getenv("16494981")
api_hash = os.getenv("71a3b460f5396bd5b5fe23139407c487")
bot_token = os.getenv("5701549938:AAGZTK-B5XcAUlWvVEAM-2T924LqKf2ZJK0")
bot = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@bot.on_message(filters.command("start"))
def start(client, message):
    text = "Hi there!\n\n" \
           "Welcome to @TheQuietBot. This bot provides real-time price updates for various cryptocurrencies.\n\n" \
           "Here are the available commands:\n\n" \
           "/price <coin> - Get the current price of a specific cryptocurrency\n\n" \
           "All prices are in USD.\n\n" \
           "Thank you for using @TheQuietBot! \n\n" \
            "Bot Made By @TheAnonxD" 
    client.send_message(chat_id=message.chat.id, text=text)

# Function to handle the /price command
@bot.on_message(filters.command("price"))
def price(client, message):
    # Extract the coin name from the message
    coin = message.text.split()[1].lower()

    # Get the price of the coin
    try:
        # Make request to Coin Gecko API
        url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={coin}"
        response = requests.get(url)
        data = response.json()[0]

        # Extract the price and percentage change data
        price = data["current_price"]
        percent_change_24h = data["price_change_percentage_24h"]

        # Format the price and percentage change data as a string
        price_formatted = f"${price:,.2f}"
        if percent_change_24h < 0:
            percent_change_formatted = f"🔻{percent_change_24h:.2f}%"
        elif percent_change_24h > 0:
            percent_change_formatted = f"🟢{percent_change_24h:.2f}%"
        else:
            percent_change_formatted = f"{percent_change_24h:.2f}%"

        message = f"<b>{data['name']} ({data['symbol'].upper()})</b>\n" \
                  f"<a href='{data['image']}'>&#8205;</a>{price_formatted}\n" \
                  f"{percent_change_formatted}"

    except (KeyError, IndexError):
        message = f"Sorry, {coin} is not a valid cryptocurrency."

    # Send the price message with HTML formatting
    client.send_message(chat_id=message.chat.id, text=message, parse_mode="HTML")

    # Start the bot
     app.run()
