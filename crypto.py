import ccxt
import matplotlib.pyplot as plt
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Set up the Telegram bot
TOKEN = '5701549938:AAGZTK-B5XcAUlWvVEAM-2T924LqKf2ZJK0'
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Define the command handler function
def send_data(bot, update):
    chat_id = update.message.chat_id
    message = update.message.text
    symbol = message.upper()
    try:
        exchange = ccxt.binance()
        
        # Fetch the ticker data
        ticker = exchange.fetch_ticker(symbol)
        price = ticker['last']
        
        # Send the data to the user
        bot.send_message(chat_id=chat_id, text=f"{symbol} Price: {price}")
        generate_chart(symbol)
        bot.send_photo(chat_id=chat_id, photo=open(symbol.upper() + '_hourly_chart.png', 'rb'))
    except:
        bot.send_message(chat_id=chat_id, text='Invalid symbol. Please try again.')

# Define the chart generator function
def generate_chart(symbol):
    exchange = ccxt.binance()
    
    # Fetch the hourly OHLCV data
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe='1h', limit=24)
    timestamps = [t[0] for t in ohlcv]
    dates = [datetime.datetime.fromtimestamp(t/1000) for t in timestamps]
    closes = [t[4] for t in ohlcv]
    
    # Generate the chart
    fig, ax = plt.subplots()
    ax.plot(dates, closes)
    ax.set_title(f'{symbol} Hourly Chart')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price (USDT)')
    fig.autofmt_xdate()
    plt.savefig(f'{symbol.upper()}_hourly_chart.png')

# Set up the command handler
dispatcher.add_handler(CommandHandler('crypto', send_data))

# Start the bot
updater.start_polling()
