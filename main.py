# -*- coding: utf-8 -*-
import StringIO
import json
import logging
import random
import urllib
import urllib2
import datetime

# for sending images
from PIL import Image
import multipart

# standard app engine imports
from google.appengine.api import urlfetch
from google.appengine.ext import ndb
import webapp2

import bottoken
import foodstore
import myutils
import botenabler

TOKEN = bottoken.get_token()

BASE_URL = 'https://api.telegram.org/bot' + TOKEN + '/'

# ================================

class CoffeeStore(ndb.Model):
    timesDrank = ndb.IntegerProperty()

def handleCoffee(name, date):
    smilies = [u'\ud83d\ude43',u'\ud83d\ude0f',u'\ud83d\ude31',u'\ud83d\ude21']
    date_got = datetime.datetime.fromtimestamp(int(date)).strftime("%Y-%m-%d")
    key = '' + name + ':coffee:' + date_got
    queryCoffee = ndb.Key('CoffeeStore', key).get()

    logging.info('key: ' + key)
    logging.info('queryCoffee.timesDrank: ' + str(queryCoffee))

    amountDrank = 0
    if queryCoffee is None:
        amountDrank = 1
    else:
        amountDrank = queryCoffee.timesDrank + 1

    coffeeDrank = CoffeeStore(key=ndb.Key('CoffeeStore', key),timesDrank=amountDrank)
    coffeeDrank.put()

    if amountDrank == 3:
        str_to_reply = name + ' drank ' + str(amountDrank) + ' coffee out of ' + str(3) + '\nIt\'s your last one !'
    elif amountDrank > 3:
        str_to_reply = name + ' drank ' + str(amountDrank) + ' coffee out of ' + str(3) + '\nPlease don\'t drink anymore...'
    else:
        str_to_reply = name + ' drank ' + str(amountDrank) + ' coffee out of ' + str(3) + '.'

    str_to_reply += ' ' + smilies[min(amountDrank-1,len(smilies)-1)]
    logging.info('reply: ' + str_to_reply)
    return str_to_reply

def updateCoffee(name, date, amount):
    date_got = datetime.datetime.fromtimestamp(int(date)).strftime("%Y-%m-%d")
    key = '' + name + ':coffee:' + date_got

    coffeeDrank = CoffeeStore(key=ndb.Key('CoffeeStore', key),timesDrank=amount)
    coffeeDrank.put()

# ================================

class MeHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'getMe'))))


class GetUpdatesHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'getUpdates'))))


class SetWebhookHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        url = self.request.get('url')
        if url:
            self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'setWebhook', urllib.urlencode({'url': url})))))


class WebhookHandler(webapp2.RequestHandler):
    def post(self):
        str_to_reply = ''
        urlfetch.set_default_fetch_deadline(60)
        body = json.loads(self.request.body)
        logging.info('request body:')
        logging.info(body)
        self.response.write(json.dumps(body))

        update_id = body['update_id']
        try:
            message = body['message']
        except:
            message = body['edited_message']
        message_id = message.get('message_id')
        date = message.get('date')
        text = message.get('text')
        fr = message.get('from')
        name = fr.get('first_name')
        chat = message['chat']
        chat_id = chat['id']
        logging.info(chat_id)

        if not text:
            logging.info('no text')
            return

        def reply(msg=None, img=None):
            logging.info(msg)
            if msg:
                resp = urllib2.urlopen(BASE_URL + 'sendMessage', urllib.urlencode({
                    'chat_id': str(chat_id),
                    'text': msg.encode('utf-8'),
                    'disable_web_page_preview': 'true',
                    'reply_to_message_id': str(message_id),
                })).read()
            elif img:
                resp = multipart.post_multipart(BASE_URL + 'sendPhoto', [
                    ('chat_id', str(chat_id)),
                    ('reply_to_message_id', str(message_id)),
                ], [
                    ('photo', 'image.jpg', img),
                ])
            else:
                logging.error('no msg or img specified')
                resp = None

            logging.info('send response:')
            logging.info(resp)

        if text.startswith('/'):
            if text == '/start':
                reply('Bot enabled')
                botenabler.setEnabled(chat_id, True)
            elif text == '/stop':
                reply('Bot disabled')
                botenabler.setEnabled(chat_id, False)
            elif text == '/image':
                img = Image.new('RGB', (512, 512))
                base = random.randint(0, 16777216)
                pixels = [base+i*j for i in range(512) for j in range(512)]  # generate sample image
                img.putdata(pixels)
                output = StringIO.StringIO()
                img.save(output, 'JPEG')
                reply(img=output.getvalue())
            elif text.startswith('/addfood'):
                # exempale: /addfood walnut 30
                str_to_reply = 'Didn\'t fully understand. Should be like: /addfood walnut 30'
                splitText = text.split()
                if len(splitText) == 3:
                    str_to_reply = foodstore.addFood(splitText[1], splitText[2])
                reply(str_to_reply)
            elif text.startswith('/showfoods'):
                reply(foodstore.showListOfFoods())
            else:
                reply('What command?')

        # CUSTOMIZE FROM HERE

        elif 'who are you' in text:
            reply('telebot starter kit, created by yukuku: https://github.com/yukuku/telebot')
        elif 'what time' in text:
            reply('look at the corner of your screen!')
        elif u'\u2615\ufe0f' in text:
            logging.info('Inside the coffee...')
            str_to_reply = handleCoffee(name, date)
            reply(str_to_reply)
        elif 'baskobot update coffee' in text:
            logging.info('Inside the update coffee...')
            str_to_reply = '' + name + ', didn\'t quite get the amount...'
            splitText = text.split()
            if len(splitText) > 3 and myutils.is_number(splitText[3]):
                updateCoffee(name, date, int(splitText[3]))
                str_to_reply = '' + name + ', the coffee amount was updated.'
            reply(str_to_reply)
        else:
            if botenabler.getEnabled(chat_id):
                reply('I got your message! (but I do not know how to answer)')
                logging.info(text)
            else:
                logging.info('not enabled for chat_id {}'.format(chat_id))


app = webapp2.WSGIApplication([
    ('/me', MeHandler),
    ('/updates', GetUpdatesHandler),
    ('/set_webhook', SetWebhookHandler),
    ('/webhook', WebhookHandler),
], debug=True)
