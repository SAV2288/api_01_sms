import time
import os

import requests
from twilio.rest import Client

from dotenv import load_dotenv 
load_dotenv()


def get_status(user_id):
    params = {
    'user_ids': user_id,
    'v': 5.92,
    'access_token': os.getenv('VK_TOKEN'),
    'fields':'online',
    }
    user_status = requests.post(f'https://api.vk.com/method/users.get',params=params).json()['response'][0]['online']
    return user_status  # Верните статус пользователя в ВК


def sms_sender(sms_text):
    account_sid = os.environ['ACCOUNT_SID']
    auth_token = os.environ['AUTH_TOKEN']
    number_from = os.environ['NUMBER_FROM']
    number_to = os.environ['NUMBER_TO']

    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                        body=sms_text,
                        from_=number_from,
                        to=number_to
                    )

    return message.sid  # Верните sid отправленного сообщения из Twilio


if __name__ == "__main__":
    vk_id = input("Введите id ")
    while True:
        if get_status(vk_id) == 1:
            sms_sender(f'{vk_id} сейчас онлайн!')
            break
        time.sleep(5)