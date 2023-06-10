import os
from bardapi import Bard

from utils.utils import write_json


def summarize_df(df):

    df_csv = df.to_csv(index=False, encoding='utf-8-sig')
    prompt = "Summarize the chat between triple quotes in detail and give your opinion"

    query = f"{prompt}\n'''\n{df_csv}\n'''"

    chat_summary = get_summary(query)
    return chat_summary


def get_summary(query):

    # if os.environ.get('SUMMARIZER') == 'BARD':
    #     chat_summary = Bard().get_answer(query)['content']
    # use OPENAI GPT3
    # else:
    #     chat_summary = Bard().get_answer(query)['content']

    chat_summary = Bard().get_answer(query)['content']
    write_json({'query': query, 'response': chat_summary})
    return chat_summary
