import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from emoji import emojize

# Initialize the Pyrogram client
api_id = 16494981 # replace with your API ID
api_hash = "71a3b460f5396bd5b5fe23139407c487" # replace with your API Hash
bot_token = "5701549938:AAGZTK-B5XcAUlWvVEAM-2T924LqKf2ZJK0" # replace with your Bot token
bot = Client("my_bot", api_id, api_hash, bot_token=bot_token)


# Function to handle the /start command
@bot.on_message(filters.command("start"))
def start(client, message):
    client.send_message(chat_id=message.chat.id, text="Hi! I'm a cryptocurrency price bot @TheQuietBot. Use the /price command followed by the name of a cryptocurrency to get its current price.Made By @TheAnonxD")


# Function to handle the /price command
@bot.on_message(filters.command("price") & filters.text)
def price(client, message):
from the message
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

        # Format the price and percentage change data as a string with red/green arrow emojis
        percent_change_24h_formatted = f"{percent_change_24h:+,.2f}%\u2193" if percent_change_24h < 0 else f"{percent_change_24h:+,.2f}%\u2191"
        message = f"<b>{data['name']} ({data['symbol'].upper()})</b>\n" \
                  f"<a href='{data['image']}'>&#8205;</a>${price:,.2f}\n" \
                  f"{percent_change_24h_formatted}"

    except (KeyError, IndexError):
        message = f"Sorry, {coin} is not a valid cryptocurrency."

    # Send the price message with HTML formatting and red/green arrow emojis
    color = "red" if percent_change_24h < 0 else "green"
    client.send_message(chat_id=message.chat.id, text=message, parse_mode="HTML", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"{percent_change_24h_formatted} {color} {emojize(':chart_with_upwards_trend:' if percent_change_24h > 0 else ':chart_with_downwards_trend:')}", callback_data="none")]]))

# Start the bot
bot.run()
