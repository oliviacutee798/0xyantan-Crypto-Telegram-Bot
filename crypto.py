import requests
from bs4 import BeautifulSoup
from telegram.ext import Updater, CommandHandler

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
updater = Updater('5701549938:AAGZTK-B5XcAUlWvVEAM-2T924LqKf2ZJK0', use_context=True)

# Define a list of authorized users
AUTHORIZED_USERS = ['@TheAnonxD']

def scrape_website(update, context):
    # Check if the user who issued the command is authorized
    user = update.effective_user.username
    if user not in AUTHORIZED_USERS: 
        context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, you are not authorized to use this command.")
        return

    url = "https://www.example.com"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all the links on the page
    links = []
    for link in soup.find_all('a'):
        links.append(link.get('href'))

    # Find all the headings on the page
    headings = []
    for heading in soup.find_all(['h1', 'h2', 'h3']):
        headings.append(heading.text)

    # Find all the images on the page
    images = []
    for img in soup.find_all('img'):
        images.append(img.get('src'))

    # Send the results to your Telegram group
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text="Links:\n{}\n\nHeadings:\n{}\n\nImages:\n{}".format(links, headings, images))

updater.dispatcher.add_handler(CommandHandler('scrape', scrape_website))
updater.start_polling()
