from pyrogram 
import Client
import requests
import filters

api_id = 16494981 # Your API ID
api_hash = "71a3b460f5396bd5b5fe23139407c487" # Your API Hash

app = Client("my_account", api_id, api_hash)

@app.on_message(filters.command("price", prefixes="!"))
def send_crypto_price(client, message):
    text = message.text.split()[1].lower()
    price = get_crypto_price(text)
    response = f"The current price of {text.upper()} is ${price:.6f}"
    message.reply(response)

def get_crypto_price(coin):
    url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={coin}&order=market_cap_desc&per_page=1&page=1&sparkline=false"
    response = requests.get(url)
    response_json = json.loads(response.text)
    price = response_json[0]["current_price"]
    market_cap = response_json[0]["market_cap"]
    volume_24h = response_json[0]["total_volume"]
    high_24h = response_json[0]["high_24h"]
    low_24h = response_json[0]["low_24h"]
    price_change_24h = response_json[0]["price_change_percentage_24h"]
    buy_volume = response_json[0]["buy_volume"]
    sell_volume = response_json[0]["sell_volume"]
    return price, market_cap, volume_24h, high_24h, low_24h, price_change_24h, buy_volume, sell_volume


@app.on_message(filters.command("price", prefixes="/"))
def send_crypto_price(client, message):
    text = message.text.split()[1].lower()
    price, market_cap, volume_24h, high_24h, low_24h, price_change_24h, buy_volume, sell_volume = get_crypto_price(text)
    response = f"*{text.upper()} Price Information:*\n\n" \
               f"💰 Current Price: *${price:.2f}*\n" \
               f"🌎 Market Cap: *${market_cap:,.0f}*\n" \
               f"📈 24H High: *${high_24h:.2f}*\n" \
               f"📉 24H Low: *${low_24h:.2f}*\n" \
               f"📈 24H % Change: *{price_change_24h:.2f}%*\n" \
               f"📈 24H Volume: *${volume_24h:,.0f}*\n" \
               f"👨‍💼 Buy Volume: *{buy_volume:,.0f}*\n" \
               f"👩‍💼 Sell Volume: *{sell_volume:,.0f}*"
    message.reply(response, parse_mode="markdown")
