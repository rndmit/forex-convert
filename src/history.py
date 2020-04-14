import os, datetime
from click import echo
from config import HISTORY_FILE


'''
Запись в историю
'''
def write_history(src_ticker, trg_ticker, amount, rate, result):
    record = f'{datetime.datetime.now()} конвертировал {amount} {src_ticker} в {trg_ticker} по курсу {rate} и получил {result} {trg_ticker} \n'
    with open(HISTORY_FILE, 'a') as history_file:
        history_file.write(record)

'''
Чтение из истории
'''
def get_history():
    with open(HISTORY_FILE, 'r') as history_file:
        for i in history_file.readlines():
            echo(i)