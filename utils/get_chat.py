import requests
import sys
import argparse


chat_url_temp = 'https://api.telegram.org/bot{}/getChat?chat_id={}'

parser = argparse.ArgumentParser(description="Extact chat_id details")
parser.add_argument('bot_token', help='The token of the bot')
parser.add_argument('-c', '--chat_id', help='chat_id for the details')
parser.add_argument('-f', '--input_file', help='File that contains a chat_id in each line')

args = parser.parse_args()

if args.chat_id and args.input_file:
    print('Only one argument should be specified: [chat_id, input_file]')
    exit(1)
elif not args.chat_id and not args.input_file:
    print('One argument should be specified: [chat_id, input_file]')
    exit(1)

print('Arguments: {}'.format(args))

if args.chat_id:
    chat_url = chat_url_temp.format(args.bot_token, args.chat_id)
    res = requests.get(chat_url)
    print(res.text)
else:
    with open(args.input_file, 'r') as f:
        for line in f:
            chat_id = line.strip()
            chat_url = chat_url_temp.format(args.bot_token, chat_id)
            res = requests.get(chat_url)
            print('{} -> {}'.format(chat_id, res.text))
