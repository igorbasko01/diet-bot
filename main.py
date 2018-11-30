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
import coffeestore
from commander import Commander

TOKEN = bottoken.get_token()

BASE_URL = 'https://api.telegram.org/bot' + TOKEN + '/'

commander = Commander()
foodstore.registerFoodStoreCommands(commander)
coffeestore.registerCoffeeCommands(commander)

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
        request_body = body
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

        cmd, params = myutils.split_text(text)
        params_encoded = [ x.encode('utf-8') for x in params]
        logging.info('Cmd: {}, Params: {}',cmd, params_encoded)

        replies = myutils.handle_message(commander, cmd, request_body, params)

        for r in replies:
            reply(r)

        if text.startswith('/'):
            if text == '/start':
                reply('Bot enabled')
                botenabler.setEnabled(chat_id, True)
            elif text == '/stop':
                reply('Bot disabled')
                botenabler.setEnabled(chat_id, False)


        # CUSTOMIZE FROM HERE


app = webapp2.WSGIApplication([
    ('/me', MeHandler),
    ('/updates', GetUpdatesHandler),
    ('/set_webhook', SetWebhookHandler),
    ('/webhook', WebhookHandler),
], debug=True)
