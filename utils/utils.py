import pandas as pd
from better_profanity import profanity
import json
import os

def format_msg_data(msg_data, username=None):
    with open("data/output.json", "w") as f:
        json.dump(json.loads(str(msg_data)), f, indent=4)
    df = pd.DataFrame(columns=['datetime', 'name', 'username', 'msg_id', 'message', 'replied_to'])
    for msg in msg_data:
        if msg.empty or msg.from_user.is_bot or ( msg.media and not msg.caption):
            continue

        df.loc[len(df)] = [msg.date, msg.from_user.first_name, msg.from_user.username, msg.id,
                           msg.text if msg.text else msg.caption, msg.reply_to_message.id if msg.reply_to_message else -1]

    df = df[~df.message.isna()]
    df.message.replace(',', '', inplace=True)

    if username:
        df = df[df.username.isin([username[1:]])]

    df.message = df.message.str.encode('utf-16').str.decode('utf-16').apply(profanity.censor)
    # df.message = df.message.apply(profanity.censor)

    return df

async def fetch_msgs_after_reply(client, app, message, limit=200):

    initial_message, post_prompt = check_post_prompt(message.text)
    msg_id_from_reply = message.reply_to_message.id
    sent_message = await message.reply('Fetching all messages after this message....', reply_to_message_id=msg_id_from_reply)
    current_message = min(limit, message.id - msg_id_from_reply)
    msg_data = await app.get_messages(int(message.chat.id), list(range(msg_id_from_reply,msg_id_from_reply + current_message - 1)))

    df = format_msg_data(msg_data)

    return df, limit, sent_message, post_prompt


async def fetch_msg_data(client, app, message, limit=100):

    sent_message = await message.reply('Processing......')
    username = None

    # Checks if there is any post prompt in the message
    initial_message, post_prompt = check_post_prompt(message.text)

    # checks if there is any default limit of messages
    if len(initial_message.split(' ')) == 2 and initial_message.split(' ')[1].isdigit():
        limit = 200 if int(initial_message.split(' ')[1]) > 200 else int(initial_message.split(' ')[1])

        await client.edit_message_text(chat_id=message.chat.id, message_id=sent_message.id,
                                       text=f'Fetching {limit} messages......')

    # checks if there is any username in the message
    elif len(initial_message.split(' ')) == 2 and initial_message.split(' ')[1][0] == '@':
        username = message.text.split(' ')[1]
        await client.edit_message_text(chat_id=message.chat.id, message_id=sent_message.id,
                                       text=f'Fetching messages of {username}......')
    else:
        await client.edit_message_text(chat_id=message.chat.id, message_id=sent_message.id,
                                       text=f'Fetching previous {limit} messages......')

    msg_data = await app.get_messages(int(message.chat.id), list(range(message.id - limit, message.id)))
    df = format_msg_data(msg_data, username)

    return df, limit, sent_message, post_prompt

async def create_query_from_ocr_data(message, ocr_chat):

    text, post_prompt = check_post_prompt(message.text)
    pre_prompt = 'Below is a chat conversation'
    if not post_prompt:
        pre_prompt = 'Generate flirty and funny replies I can use to send the opposite person'
    query = f"{pre_prompt}\n'''\n{ocr_chat}\n'''\n{post_prompt}"
    return query


def write_json(new_data):
    filename = 'data/prompts.json'
    with open(filename, 'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)

        # Join new_data with file_data inside emp_details
        file_data.append(new_data)

        # Sets file's current position at offset.
        file.seek(0)

        # convert back to json.
        json.dump(file_data, file, indent=4)


def create_prompt_files():
    if 'prompts.json' not in os.listdir('data'):
        empty_list = []
        # Convert the list to a JSON object
        list_of_items = []

        # Write the list to a JSON file
        filename = 'data/prompts.json'
        with open(filename, "w") as f:
            json.dump(list_of_items, f, indent=4)


def check_post_prompt(text):
    if 'query:' in text.lower():
        return [s.strip() for s in text.split('query:')]
    else:
        return text, None