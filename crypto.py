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


@bot.on_message(filters.command("price") & filters.text)
def price(client, message):
    coin = message.text.split()[1].lower()

    try:
        response = requests.get(f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={coin}")
        data = response.json()
        price = data[0]["current_price"]
        percent_change_24h = data[0]["price_change_percentage_24h"]
        symbol = data[0]["symbol"].upper()

        if percent_change_24h > 0:
            color = "\U0001F7E2"
        else:
            color = "\U0001F534"

        percent_change_24h_formatted = f"{percent_change_24h:.2f}%"

        message = f"{emojize(':money_with_wings:', use_aliases=True)} <b>{coin.upper()}</b> ({symbol})\n\nPrice: ${price:,.2f}\n24h: {percent_change_24h_formatted} {color} {emojize(':chart_with_upwards_trend:' if percent_change_24h > 0 else ':chart_with_downwards_trend:')}"
        client.send_message(chat_id=message.chat.id, text=message, parse_mode="HTML", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"{percent_change_24h_formatted} {color} {emojize(':chart_with_upwards_trend:' if percent_change_24h > 0 else ':chart_with_downwards_trend:')}", callback_data="none")]]))

    except Exception as e:
        message = f"{emojize(':warning:', use_aliases=True)} Error retrieving data for <b>{coin.upper()}</b>. Please check the spelling of the coin and try again."
        client.send_message(chat_id=message.chat.id, text=message, parse_mode="HTML")

    client.send_message(chat_id=message.chat.id, text=message, parse_mode="HTML", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"{percent_change_24h_formatted} {color} {emojize(':chart_with_upwards_trend:' if percent_change_24h > 0 else ':chart_with_downwards_trend:')}", callback_data="none")]]))

# Start the bot
bot.run()
