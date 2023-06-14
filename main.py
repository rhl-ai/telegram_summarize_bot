import os

import numpy as np
import cv2
from pyrogram import Client, filters
from utils.utils import fetch_msg_data,create_prompt_files, fetch_msgs_after_reply, create_query_from_ocr_data
from utils.summary_utils import summarize_df, get_summary
from utils.message_utils import replied_msg_data, fetch_text
from utils.image_util import image_to_ocr_conversation, image_to_ocr_text
from utils.const import help_text
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
    df, limit, sent_message, post_prompt = await fetch_msg_data(client, app, message, limit=100)
    if len(df) == 0:
        await client.edit_message_text(chat_id=message.chat.id, message_id=sent_message.id,
                                       text=f'No messages found')
        return

    df.to_csv('data/send_raw.csv',encoding='utf-8-sig', index=False)
    await app.send_document(chat_id=message.chat.id, document='data/send_raw.csv'
                            , caption=f"Here are the last {limit} messages")


@app.on_message(filters.command(["summarize"]))
async def summarize_chat(client, message):
    try:
        # check if message is a reply
        if message.reply_to_message:
            df, limit, sent_message, post_prompt = await fetch_msgs_after_reply(client,app, message)
        else:
            df, limit, sent_message, post_prompt = await fetch_msg_data(client, app, message, limit=100)

        if len(df) == 0:
            await client.edit_message_text(chat_id=message.chat.id, message_id=sent_message.id,text=f'No messages found')
            return

        await client.edit_message_text(chat_id=message.chat.id, message_id=sent_message.id,text=f'Summarizing total {len(df)} messages......')

        chat_summary = summarize_df(df, post_prompt)

        if 'Response Error' in chat_summary:
            chat_summary = 'Null Response, Applying secret sauce and trying again......'
            await client.edit_message_text(chat_id=message.chat.id, message_id=sent_message.id, text=chat_summary)

            # Split df in 2 parts
            df_ls = np.array_split(df, 2)
            chat_summary = summarize_df(df_ls[0], post_prompt) + '\n\nWait for next message......'
            await client.edit_message_text(chat_id=message.chat.id, message_id=sent_message.id, text=chat_summary)

            chat_summary = summarize_df(df_ls[1], post_prompt)

            await client.send_message(chat_id=message.chat.id, text=chat_summary, reply_to_message_id=sent_message.id)
            return

        await client.edit_message_text(chat_id=message.chat.id, message_id=sent_message.id, text=chat_summary)
    except Exception as e:
        await client.send_message(chat_id=message.chat.id, text=f'Error: {e}', reply_to_message_id=message.id)
@app.on_message(filters.command(['give_opinion']))
async def give_opinion(client,message):
    name, text, msg_id = replied_msg_data(message)
    if name is None:
        await message.reply("Please reply to a message")
        return

    pre_prompt = fetch_text(message)
    if pre_prompt is None:
        pre_prompt = 'Give your opinion on the below message'
    print(pre_prompt)
    prompt = f"{pre_prompt}\n\n'''\nMessage From: {name}\n\nMessage:{text}\n'''"
    opinion = get_summary(prompt)
    await message.reply(opinion, reply_to_message_id=msg_id)


@app.on_message(filters.command(['get_rizz_ocr']))
async def get_rizz_ocr(client, message):
    try:
        if not message.reply_to_message or not message.reply_to_message.photo:
            await message.reply("Please reply to an image chat conversation", reply_to_message_id=message.id)
            return

        # file_name_with_path = f'data/{message.reply_to_message.photo.file_id}.jpg'
        file_name_with_path = 'data/saved_chat_ocr_image.jpg'
        await client.download_media(message.reply_to_message.photo, file_name=file_name_with_path)
        chat_text, image = image_to_ocr_conversation(file_name_with_path)

        processed_file_name = 'data/saved_processed_image.jpg'
        cv2.imwrite(processed_file_name, image)
        await message.reply_photo('data/saved_processed_image.jpg', reply_to_message_id=message.id, caption = chat_text)
    except Exception as e:
        await client.send_message(chat_id=message.chat.id, text=f'Error: {e}', reply_to_message_id=message.id)

@app.on_message(filters.command(['get_rizz']))
async def get_rizz(client, message):
    try:
        if not message.reply_to_message or not message.reply_to_message.photo:
            await message.reply("Please reply to an image chat conversation", reply_to_message_id=message.id)
            return

        sent_message = await message.reply("Generating Rizz", reply_to_message_id=message.id)

        file_name_with_path = f'data/{message.reply_to_message.photo.file_id}.jpg'

        await client.edit_message_text(chat_id=message.chat.id, message_id=sent_message.id, text='Rizz initiation start')

        await client.download_media(message.reply_to_message.photo, file_name=file_name_with_path)
        chat_text, _ = image_to_ocr_conversation(file_name_with_path)

        await client.edit_message_text(chat_id=message.chat.id, message_id=sent_message.id, text='Consulting Dating Gurus')

        query = await create_query_from_ocr_data(message, chat_text)
        output_msg = get_summary(query)

        await client.edit_message_text(chat_id=message.chat.id, message_id=sent_message.id, text=output_msg)
    except Exception as e:
        await client.send_message(chat_id=message.chat.id, text=f'Error: {e}', reply_to_message_id=message.id)
@app.on_message(filters.command(['ocr']))
async def do_ocr(client, message):
    try:
        if not message.reply_to_message or not message.reply_to_message.photo:
            await message.reply("Please reply to an image", reply_to_message_id=message.id)
            return

        file_name_with_path = f'data/{message.reply_to_message.photo.file_id}.jpg'
        await client.download_media(message.reply_to_message.photo, file_name=file_name_with_path)
        chat_text, image = image_to_ocr_text(file_name_with_path)

        # send photo as reply to the message
        image_path = 'data/saved_processed_image.jpg'
        cv2.imwrite(image_path, image)

        if len(message.text.split(' ')) > 1:
            await message.reply_photo(image_path, reply_to_message_id=message.id, caption = chat_text)
        else:
            await message.reply(chat_text, reply_to_message_id=message.id)
    except Exception as e:
        await message.reply(f'Error: {e}', reply_to_message_id=message.id)

@app.on_message(filters.command(['start', 'help']))
async def get_help(client, message):
    await message.reply(help_text, reply_to_message_id=message.id)


if __name__ == '__main__':
    create_prompt_files()
    app.run()

