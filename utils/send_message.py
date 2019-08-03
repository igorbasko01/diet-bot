import requests
import sys
import argparse

chat_url_temp = 'https://api.telegram.org/bot{}/sendMessage'

parser = argparse.ArgumentParser(description="Send a message to a user using some telegram bot.")
parser.add_argument('bot_token', help='The token of the bot')
parser.add_argument('chat_id', help='To whom to send the message')
parser.add_argument('message', help='The message to send')

args = parser.parse_args()

data = {'chat_id': args.chat_id, 'text': args.message}

res = requests.post(chat_url_temp.format(args.bot_token), data=data)

print(res)
print(res.text)
