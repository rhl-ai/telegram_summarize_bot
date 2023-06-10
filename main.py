import os

import numpy as np

from pyrogram import Client, filters
from utils.utils import fetch_msg_data,create_prompt_files
from utils.summary_utils import summarize_df, get_summary
from utils.message_utils import replied_msg_data, fetch_text

from dotenv import load_dotenv
load_dotenv()

app = Client(
    "pyrogram",
    api_id=int(os.environ.get('API_ID', 12345 )),
    api_hash=os.environ.get('API_HASH','' ),
    bot_token=os.environ.get('BOT_TOKEN','' )
)



@app.on_message(filters.command(["askb"]))
async def run_bard(client, message):
    sent_message = await message.reply('Processing......', reply_to_message_id=message.id)

    print(message.text)
    if len(message.text.split(' ')) < 2:
        await message.reply("Please enter a query")
    else:
        query = " ".join(message.text.split(' ')[1:])

        output_msg = get_summary(query)

        await client.edit_message_text(chat_id=message.chat.id, message_id=sent_message.id, text=output_msg)


@app.on_message(filters.command(["send_raw"]))
async def send_raw(client, message):
    df, limit, sent_message = await fetch_msg_data(client, app, message, limit=100)
    if len(df) == 0:
        await client.edit_message_text(chat_id=message.chat.id, message_id=sent_message.id,
                                       text=f'No messages found')
        return

    df.to_csv('data/send_raw.csv',encoding='utf-8-sig', index=False)
    await app.send_document(chat_id=message.chat.id, document='data/send_raw.csv'
                            , caption=f"Here are the last {limit} messages")


@app.on_message(filters.command(["summarize"]))
async def summarize_chat(client, message):
    df, limit, sent_message = await fetch_msg_data(client, app, message, limit=100)
    if len(df) == 0:
        await client.edit_message_text(chat_id=message.chat.id, message_id=sent_message.id,text=f'No messages found')
        return

    await client.edit_message_text(chat_id=message.chat.id, message_id=sent_message.id,text=f'Summarizing total {len(df)} messages......')

    chat_summary = summarize_df(df)

    if 'Response Error' in chat_summary:
        chat_summary = 'Null Response, Applying secret sauce and trying again......'
        await client.edit_message_text(chat_id=message.chat.id, message_id=sent_message.id, text=chat_summary)

        # Split df in 2 parts
        df_ls = np.array_split(df, 2)
        chat_summary = summarize_df(df_ls[0]) + '\n\nWait for next message......'
        await client.edit_message_text(chat_id=message.chat.id, message_id=sent_message.id, text=chat_summary)

        chat_summary = summarize_df(df_ls[1])

        await client.send_message(chat_id=message.chat.id, text=chat_summary, reply_to_message_id=sent_message.id)
        return

    await client.edit_message_text(chat_id=message.chat.id, message_id=sent_message.id, text=chat_summary)

@app.on_message(filters.command(['give_opinion']))
async def give_opinion(client,message):
    name, text, msg_id = replied_msg_data(message)
    if name is None:
        await message.reply("Please reply to a message")
        return

    pre_prompt = fetch_text(message)
    if pre_prompt is None:
        pre_prompt = 'Give your opinion on the below message'
    prompt = f"{pre_prompt}\n\n'''\nMessage From: {name}\n\nMessage:{text}\n'''"
    opinion = get_summary(prompt)
    await message.reply(opinion, reply_to_message_id=msg_id)


@app.on_message(filters.command(['start', 'help']))
async def get_help(client, message):
    await message.reply("Available commands:\n\n"
                        "/summarize - Summarize the last 100 messages\n"
                        "/summarize number - Summarize the last <number> messages\n"
                        "/summarize username - Summarize the last 100 messages by a user\n"
                        "/send_raw - Send the last 100 messages as csv\n"
                        "/send_raw number - Send the last <number> messages as csv\n"
                        "/give_opinion - Give opinion on the replied message\n"
                        "/give_opinion query - Give your opinion based on the prompt on the replied message\n"
                        "/askb query - Ask a question to bard\n"
                        "/help - Get help")


if __name__ == '__main__':
    create_prompt_files()
    app.run()

