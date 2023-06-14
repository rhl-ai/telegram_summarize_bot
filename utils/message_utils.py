

def replied_msg_data(message):
    if message.reply_to_message:
        return message.reply_to_message.from_user.first_name, \
            message.reply_to_message.caption if message.reply_to_message.caption else message.reply_to_message.text, \
            message.reply_to_message.id
    else:
        return None, None, None

def fetch_text(message):
    if len(message.text.split(" ")) == 1:
        return None
    else:
        return " ".join(message.text.split(" ")[1:])