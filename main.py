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

class BotToken(ndb.Model):
    token = ndb.StringProperty();
    
queriedToken = ndb.Key('BotToken', 'dietbottoken').get()
tokenMessage = 'No token was found !'
if queriedToken is not None:
    tokenMessage = 'Token Found !'
logging.info(tokenMessage)

TOKEN = queriedToken.token

BASE_URL = 'https://api.telegram.org/bot' + TOKEN + '/'

# ================================

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

# ================================

class EnableStatus(ndb.Model):
    # key name: str(chat_id)
    enabled = ndb.BooleanProperty(indexed=False, default=False)


# ================================

def setEnabled(chat_id, yes):
    es = EnableStatus.get_or_insert(str(chat_id))
    es.enabled = yes
    es.put()

def getEnabled(chat_id):
    es = EnableStatus.get_by_id(str(chat_id))
    if es:
        return es.enabled
    return False


# ================================

# Stores a list of different foods that the user configured.
# Used as an index, to know which foods exists in the system.
class FoodsListStore(ndb.Model):
    listOfNames = ndb.StringProperty()

def showListOfFoods():
    queryFoodList = ndb.Key('FoodsListStore', 'FoodsList').get()
    foodList = 'No foods !'
    if not queryFoodList is None:
        foodList = queryFoodList.listOfNames
    return foodList

def addFood(foodName, calories):
    if not is_number(calories) or int(calories) < 1:
        return 'Invalid calories ! should be a number greater than 0.'

    result_msg = ''

    # Get list of food names.
    queryFoodList = ndb.Key('FoodsListStore', 'FoodsList').get()
    foodsListArray = []
    if not queryFoodList is None:
        foodsListArray = queryFoodList.listOfNames.split(',')
    logging.info('Got food list: ' + str(foodsListArray))

    # add the new food only if its not already in the list.
    if not foodName in foodsListArray:
        foodsListArray.append(foodName)
        foodsListString = ",".join(foodsListArray)
        foodsList = FoodsListStore(key=ndb.Key('FoodsListStore', 'FoodsList'),listOfNames=foodsListString)
        foodsList.put()
        result_msg = 'Food ' + foodName + ' added, calories: ' + str(calories) + '.'
    else:
        result_msg = 'Food ' + foodName + ' already exists...'

    return result_msg

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
                setEnabled(chat_id, True)
            elif text == '/stop':
                reply('Bot disabled')
                setEnabled(chat_id, False)
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
                    str_to_reply = addFood(splitText[1], splitText[2])
                reply(str_to_reply)
            elif text.startswith('/showfoods'):
                reply(showListOfFoods())
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
            if len(splitText) > 3 and is_number(splitText[3]):
                updateCoffee(name, date, int(splitText[3]))
                str_to_reply = '' + name + ', the coffee amount was updated.'
            reply(str_to_reply)
        else:
            if getEnabled(chat_id):
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
