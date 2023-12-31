import requests
import os
from time import sleep
from input_mobile import send_sms
from dotenv import load_dotenv
from pymongo import MongoClient, DESCENDING

load_dotenv()

client = MongoClient(os.environ['MONGODB_URI'])
db = client['input_mobile']
messages = db['telegram']


def send_message(text, chat_id=os.environ["TELEGRAM_CHAT_ID"]):
    url = f'https://api.telegram.org/bot{os.environ["TELEGRAM_TOKEN"]}/sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    r = requests.post(url, json=payload)
    return r


def set_webhook(url=os.environ["TELEGRAM_WEBHOOK_URL"]):
    u = f'https://api.telegram.org/bot{os.environ["TELEGRAM_TOKEN"]}/' \
        f'setWebhook?url={url}'
    return requests.get(u)


def read_last_message():
    record = list(messages.find().sort("created_at", DESCENDING).limit(1))
    if record is None or len(record) == 0:
        return None
    return record[0]['text']


def input_(
        prompt: str = None,
        timeout: int = 60,
        pooling_freq: int = 1,
        alert_via_sms: bool = True,
        debug: bool = False
) -> str:
    if prompt is not None:
        send_message(prompt)
        if alert_via_sms:
            send_sms(f'You received the prompt "{prompt}" on Telegram. '
                     f'You have {timeout} seconds to answer it.')

    messages.delete_many({})
    if debug:
        print(f'\rWaiting for reply in Telegram ({timeout}s)...', end='')

    sleep(1)
    for i in range(timeout):
        if debug:
            print(f'\rWaiting for reply in Telegram ({timeout - i}s)...', end='')

        content = read_last_message()
        if content is not None:
            messages.delete_many({})
            if debug:
                print(' Reply sent. Returning to the program.')
            return content
        sleep(pooling_freq)

    messages.delete_many({})
    if debug:
        print(' Timeout. Returning to the program.')

    return None


def send_photo(filename, chat_id=os.environ["TELEGRAM_CHAT_ID"]):
    url = f'https://api.telegram.org/bot{os.environ["TELEGRAM_TOKEN"]}/sendPhoto'
    payload = {'chat_id': chat_id}
    files = {'photo': open(filename, 'rb')}
    r = requests.post(url, data=payload, files=files)
    return r

