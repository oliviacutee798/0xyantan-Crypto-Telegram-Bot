import requests
import json
from telegram.ext import Updater, CommandHandler

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the crypto price bot!")

def get_price(update, context):
    symbol = context.args[0].upper()
    url = "https://min-api.cryptocompare.com/data/price?fsym={}&tsyms=USD".format(symbol)
    response = requests.get(url)
    data = json.loads(response.text)
    price = data["USD"]
    message = "The price of {} is {} USD".format(symbol, price)
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def main():
    updater = Updater(token='5701549938:AAGZTK-B5XcAUlWvVEAM-2T924LqKf2ZJK0', use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("price", get_price))
    updater.start_polling()
    updater.idle()

if name == 'main':
    main()
