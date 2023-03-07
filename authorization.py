from pyrogram import Client

api_id = 16494981
api_hash = "71a3b460f5396bd5b5fe23139407c487"
bot_token = "5701549938:AAGZTK-B5XcAUlWvVEAM-2T924LqKf2ZJK0"

app = Client(
    "my_bot",
    api_id=api_id, api_hash=api_hash,
    bot_token=bot_token
)

app.run()
