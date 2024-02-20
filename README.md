## Getcontact

This is a bot and desktop application with a server for searching contact data by phone number.

For this program to work, you need a GetContact number database or other third-party databases (you will have to rewrite the code to work with other databases).

### Telegram_bot

Modify the .env.example file:
```
TOKEN = # telegram token
USER = # mysql user
PASSWORD = # mysql password
HOST = # mysql host example: 127.0.0.1
```

Start the bot:
```
python main.py
```

### GetContact

Modify the .env.example file:
```
USER = # mysql user
PASSWORD = # mysql password
HOST = # mysql host example: 127.0.0.1
```
You need to set the server address in the server.py file (line 67):
```
app.run(port=6666)
```
__Default port is 6666__

You also need to change the server address in the main.py file (line 61):
```
‘http://127.0.0.1:6666/api’, data=data)
```
And start the server:
```
python server.py
```
