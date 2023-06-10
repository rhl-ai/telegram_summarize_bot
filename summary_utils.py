import os
from bardapi import Bard

from utils import write_json

os.environ['_BARD_API_KEY'] = "WwgtZlDmzrIlN-WIeGvWgEo4GNbKNLNJ4yoJukoShZYdxu9LVUmS3rzhjC8NOAmC4AS5SQ."


def summarize_df(df):
    df_csv = df.to_csv(index=False, encoding='utf-8-sig')
    prompt = "Summarize the chat between triple quotes in detail and give your opinion"

    query = f"{prompt}\n'''\n{df_csv}\n'''"

    chat_summary = get_summary(query)
    return chat_summary


def get_summary(query):
    chat_summary = Bard().get_answer(query)['content']

    write_json({'query': query, 'response': chat_summary})
    return chat_summary
