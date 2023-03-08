import telegram
import ccxt
import pandas as pd
import mplfinance as mpf
from datetime import datetime, timedelta


def generate_chart(symbol):
    exchange = ccxt.binance()
    timeframe = '1h'
    since = exchange.milliseconds() - 86400000
    data = exchange.fetch_ohlcv(symbol, timeframe, since)
    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    mpf.plot(df, type='candle', volume=True, title=symbol.upper() + ' Hourly Chart', mav=(5,10,20))


def send_data(bot, update):
    chat_id = update.message.chat_id
    message = update.message.text
    symbol = message.upper()
    try:
        exchange = ccxt.binance()
        
        # Fetch the ticker data
        ticker = exchange.fetch_ticker(symbol)
        price = ticker['last']
        
        # Fetch the volume data for the last 5, 15, and 30 minutes
        timeframe = '1m'
        since_5 = exchange.milliseconds() - 5 * 60 * 1000
        since_15 = exchange.milliseconds() - 15 * 60 * 1000
        since_30 = exchange.milliseconds() - 30 * 60 * 1000
        trades_5 = exchange.fetch_trades(symbol, since=since_5)
        trades_15 = exchange.fetch_trades(symbol, since=since_15)
        trades_30 = exchange.fetch_trades(symbol, since=since_30)
        buy_volume_5 = sum([t['amount'] for t in trades_5 if t['side'] == 'buy'])
        sell_volume_5 = sum([t['amount'] for t in trades_5 if t['side'] == 'sell'])
        buy_volume_15 = sum([t['amount'] for t in trades_15 if t['side'] == 'buy'])
        sell_volume_15 = sum([t['amount'] for t in trades_15 if t['side'] == 'sell'])
        buy_volume_30 = sum([t['amount'] for t in trades_30 if t['side'] == 'buy'])
        sell_volume_30 = sum([t['amount'] for t in trades_30 if t['side'] == 'sell'])
        
        # Format the volume data with emojis
        up_arrow = u'\U0001F53A'
        down_arrow = u'\U0001F53B'
        volume_5 = f"{up_arrow} {buy_volume_5:.2f} / {down_arrow} {sell_volume_5:.2f}"
        volume_15 = f"{up_arrow} {buy_volume_15:.2f} / {down_arrow} {sell_volume_15:.2f}"
        volume_30 = f"{up_arrow} {buy_volume_30:.2f} / {down_arrow} {sell_volume_30:.2f}"
        
        # Send the data to the user
        bot.send_message(chat_id=chat_id, text=f"{symbol} Price: {price}")
        bot.send_message(chat_id=chat_id, text=f"Last 5m Volume: {volume_5}")
        bot.send_message(chat_id=chat_id, text=f"Last 15m Volume: {volume_15}")
        bot.send_message(chat_id=chat_id, text=f"Last 30m Volume: {volume_30}")
        generate_chart(symbol)
        bot.send_photo(chat_id=chat_id, photo=open(symbol.upper() + '_hourly_chart.png', 'rb'))
    except:
        bot.send_message(chat_id=chat_id, text='Invalid symbol. Please try again.')


# Replace YOUR_BOT_TOKEN with your actual bot token
bot = telegram.Bot(token='5701549938:AAGZTK-B5XcAUlWvVEAM-2T924LqKf2ZJK0')

def main():
    updater = telegram.Updater(token='5701549938:AAGZTK-B5XcAUlWvVEAM-2T924LqKf2ZJK0')
    dispatcher = updater.dispatcher
    dispatcher.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, send_data))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()


