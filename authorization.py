from pyrogram import Client

api_id = 16494981
api_hash = "71a3b460f5396bd5b5fe23139407c487"

app = Client("my_account", api_id=api_id, api_hash=api_hash)

app.run()
