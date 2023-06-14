# Telegram group chat summarizer
**A telegram Bot** that can summarize your **group chats** and additional fun

It uses [BARDAPI](https://github.com/dsdanielpark/Bard-API/) and [Pyrogram](https://pyrogram.org/)

You can make use of OPENAI API as well which is included in unused scripts.


## Features

### Get Rizz
* `/get_rizz` - Get Rizz for the replied image conversation
* `/get_rizz query:` **query** - Get Rizz for the replied image with your prompt

### OCR
* `/ocr` - Get OCR for the replied image
* `/ocr image_word` - Get OCR for the replied image with image

### Summarize with default prompt
* `/summarize` - Summarize the last 100 messages
* `/summarize` **number** - Summarize the last number messages
* `/summarize` - reply to a message and it summarize all messages after the replied message
* `/summarize` **@username** - Summarize the last 100 messages by a user

### Summarize with your prompt
* `/summarize query:` **query** - Summarize the last 100 messages
* `/summarize number query:` **query** - Summarize the last number messages
* `/summarize query:` **query** - reply to a message and it summarize all messages after the replied message
* `/summarize username query:` **query** - Summarize the last 100 messages by a user

### Get opinion on the message
* `/give_opinion` - Give opinion on the replied message
* `/give_opinion` **query** - Give your opinion based on the prompt on the replied message

### Ask bard
* `/askb` **query** - Ask a question to bard

### Raw text data
* `/send_raw` - Send the last 100 messages as csv
* `/send_raw` **number** - Send the last number messages as csv

### Get help
* `/help` - Get help


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
