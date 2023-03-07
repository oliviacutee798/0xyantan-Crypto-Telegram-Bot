import requests
from bs4 import BeautifulSoup
import datetime
import time
import pyrogram
from pyrogram import Client, filters
from pyrogram.types import Message

# initialize Pyrogram client
api_id = "16494981"
api_hash = "71a3b460f5396bd5b5fe23139407c487"
bot_token = "5701549938:AAGZTK-B5XcAUlWvVEAM-2T924LqKf2ZJK0"
app = Client("my_bot", api_id, api_hash, bot_token=bot_token)

# function to scrape the upcoming events from cryptocraft.com
def get_upcoming_events():
 
      timezone = pytz.timezone('Asia/Kolkata')

    url = "https://www.cryptocraft.com/calendar"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    events = []
    for event in soup.find_all("div", {"class": "ecp_tr"}):
        date = event.find_all("td")[0].text.strip()
        time = event.find_all("td")[1].text.strip()
        name = event.find_all("td")[2].text.strip()
        events.append({"date": date, "time": time, "name": name})
    return events

# function to check if an event is happening today
def is_today(event_date):
    today = datetime.datetime.now()
    event_date = datetime.datetime.strptime(event_date, "%Y-%m-%d")
    if event_date.date() == today.date():
        return True
    else:
        return False

# function to send a reminder about an event
def send_reminder(event):
    text = f"Reminder: {event['name']} is happening today at {event['time']}"
    app.send_message(chat_id="-1001833772215", text=text)

# function to run the bot
@app.on_message(filters.command("events"))
def get_events(client: Client, message: Message):
    events = get_upcoming_events()
    for event in events:
        if is_today(event["date"]):
            send_reminder(event)
            time.sleep(5) # delay between messages

# start the bot
app.run()
