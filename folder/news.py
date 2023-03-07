import requests
from bs4 import BeautifulSoup
import time
from pyrogram import Client

# Replace with your own values
api_id = 16494981
api_hash = '71a3b460f5396bd5b5fe23139407c487'
bot_token = '5701549938:AAGZTK-B5XcAUlWvVEAM-2T924LqKf2ZJK0'
chat_id = '-1001833772215'

app = Client('my_session', api_id=api_id, api_hash=api_hash, bot_token=bot_token)

def get_news():
    url = 'https://www.coindesk.com/'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    articles = soup.find_all('article')
    return articles

@app.on_message()
def forward_news(client, message):
    if message.chat.id == chat_id:
        for article in get_news():
            title = article.h4.text
            summary = article.p.text
            link = article.a['href']
            msg = f'<b>{title}</b>\n{summary}\n<a href="{link}">Read More</a>'
            client.send_message(chat_id, text=msg, parse_mode='html')
            time.sleep(2)

app.run()
