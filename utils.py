import pandas as pd
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
    return df


async def fetch_msg_data(client, app, message, limit=100):

    sent_message = await message.reply('Processing......')
    username = None
    if len(message.text.split(' ')) == 2 and message.text.split(' ')[1].isdigit():
        limit = 200 if int(message.text.split(' ')[1]) > 200 else int(message.text.split(' ')[1])

        await client.edit_message_text(chat_id=message.chat.id, message_id=sent_message.id,
                                       text=f'Fetching {limit} messages......')

    elif len(message.text.split(' ')) == 2 and message.text.split(' ')[1][0] == '@':
        username = message.text.split(' ')[1]
        await client.edit_message_text(chat_id=message.chat.id, message_id=sent_message.id,
                                       text=f'Fetching messages of {username}......')

    msg_data = await app.get_messages(int(message.chat.id), list(range(message.id - limit, message.id)))
    df = format_msg_data(msg_data, username )

    return df, limit, sent_message


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
        with open("data/prompts.json", "w") as f:
            json.dump(list_of_items, f, indent=4)
