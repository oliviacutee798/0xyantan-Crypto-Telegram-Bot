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



# Start the bot
bot.run()
