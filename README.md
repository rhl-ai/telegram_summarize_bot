# telegram_summarize_bot
**A telegram Bot** that can summarize your **group chats** and additional fun

It uses [BARDAPI](https://github.com/dsdanielpark/Bard-API/) and [Pyrogram](https://pyrogram.org/)

You can make use of OPENAI API as well which is included in unused scripts.


## Features
* Summarize your group chats
  * Type `/summarize` to get a summary of the 100 recent messages
  * Type `/summarize <number>` to get a summary of the <number> recent messages
  * Type `/summarize <username>` to get a summary of the 100 recent messages from <username>
* Type `/askb <Query>` to ask a question to the bot which uses [BARDAPI](https://github.com/dsdanielpark/Bard-API/)
* Type `/give_opinion` or `/give_opinion <prompt>`  while replying to a text to get the opinion of the bot on the text
* Type `/send_raw` or `/send_raw <number>` to get raw csv for testing

## How to Deploy 
You can Deploy it to Railway or run locally 

### Deploy to railway 

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/TPbR3E?referralCode=JiNgRe)

### Run locally 
If you want to run it locally then rename sample.env to .env
```
# BARD KEY Refer to https://github.com/dsdanielpark/Bard-API/
_BARD_API_KEY = ""

# Telegram API KEYS
# Get this value from https://my.telegram.org/apps
API_ID = 12345 # API_ID should be int
API_HASH = ""

# Create a bot from https://t.me/BotFather and enter the token here
BOT_TOKEN = ""

# Either use OPENAI or BARD
SUMMARIZER = "BARD"
```

## Acknowledgements
* [Pyrogram](https://pyrogram.org/)
* [BARDAPI](https://github.com/dsdanielpark/Bard-API/)
