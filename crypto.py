import requests
import pyrogram

# Set up the bot
bot = pyrogram.Client("my_bot", api_id=16494981, api_hash="71a3b460f5396bd5b5fe23139407c487", bot_token="5701549938:AAGZTK-B5XcAUlWvVEAM-2T924LqKf2ZJK0")

# Define the start command
@bot.on_message(pyrogram.filters.command(["start"]))
def start(bot, update):
    update.reply_text("Hi! I can retrieve the current price of a cryptocurrency. Send me the name or symbol of the cryptocurrency you're interested in.")

# Define the price command
@bot.on_message(pyrogram.filters.command(["price"]))
def price(bot, update):
    # Get the cryptocurrency name or symbol from the message
    coin = " ".join(update.text.split()[1:]).upper()

    # Make a request to the CoinMarketCap API to get the price and logo of the cryptocurrency
    response = requests.get(f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol={coin}", headers={"X-CMC_PRO_API_KEY": "0554365c-f9a4-43f3-b809-3b568f9db1db"})
    logo_response = requests.get(f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/info?symbol={coin}", headers={"X-CMC_PRO_API_KEY": "0554365c-f9a4-43f3-b809-3b568f9db1db"})

    # Parse the response and retrieve the price and logo
    data = response.json().get("data", {})
    logo_data = logo_response.json().get("data", {}).get(coin, {})
    if data:
        price = data[coin].get("quote", {}).get("USD", {}).get("price")
        logo_url = logo_data.get("logo")
    else:
        price = None
        logo_url = None

    # Respond to the user with the price and logo
    if price and logo_url:
        message = f"📈 <b>{coin}</b> is currently trading at <b>${price:.2f}</b>\n"
        message += f'<a href="{logo_url}">&#8205;</a>' # Add the coin logo to the message
        message += "\n\n<b>24h Change:</b>\n"
        percent_change_24h = data[coin].get("quote", {}).get("USD", {}).get("percent_change_24h")
        if percent_change_24h is not None:
            if percent_change_24h >= 0:
                message += f"🟢 +{percent_change_24h:.2f}%"
            else:
                message += f"🔴 {percent_change_24h:.2f}%"
        else:
            message += "N/A"
        update.reply_text(message, parse_mode=ParseMode.HTML)
    else:
        update.reply_text("Sorry, I couldn't find the price of that cryptocurrency.")

# Start the bot
bot.run()
