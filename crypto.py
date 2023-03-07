import pyrogram
import requests

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
    coin = " ".join(update.text.split()[1:]).lower()

    # Make a request to the CoinGecko API to get the price of the cryptocurrency
    response = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd")

    # Parse the response and retrieve the price
    price = response.json().get(coin, {}).get("usd")

    # Respond to the user with the price
    if price:
        update.reply_text(f"The current price of {coin.upper()} is ${price:.2f}")
    else:
        update.reply_text("Sorry, I couldn't find the price of that cryptocurrency.")

# Start the bot
bot.run()
