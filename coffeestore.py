from google.appengine.ext import ndb

import logging
import datetime
import myutils

class CoffeeStore(ndb.Model):
    timesDrank = ndb.IntegerProperty()


def registerCoffeeCommands(commander):
    commander.register_command('/coffeeupd', update_coffee)
    commander.register_command(commander.KEY_OTHER, handle_coffee)

def getCoffeeKey(name, date):
    date_got = datetime.datetime.fromtimestamp(int(date)).strftime("%Y-%m-%d")
    key = '{}:coffee:{}'.format(name, date_got)
    return key

def getCoffeeAmount(key):
    return ndb.Key('CoffeeStore', key).get()


def handle_coffee(request_body, text):
    coffees = text.count(u'\u2615\ufe0f')
    if coffees == 0:
        return ''

    name = myutils.extract_user_first_name(request_body)
    date = myutils.extract_date(request_body)

    smilies = [u'\ud83d\ude43',u'\ud83d\ude0f',u'\ud83d\ude31',u'\ud83d\ude21']
    key = getCoffeeKey(name, date)
    queryCoffee = getCoffeeAmount(key)

    logging.info('key: ' + key)
    logging.info('queryCoffee.timesDrank: ' + str(queryCoffee))
    logging.info('Coffees to add: {}'.format(coffees))

    amount_drank = coffees
    if queryCoffee is not None:
        amount_drank += queryCoffee.timesDrank

    coffeeDrank = CoffeeStore(key=ndb.Key('CoffeeStore', key),timesDrank=amount_drank)
    coffeeDrank.put()

    if amount_drank == 3:
        str_to_reply = name + ' drank ' + str(amount_drank) + ' coffee out of ' + str(3) + '\nIt\'s your last one !'
    elif amount_drank > 3:
        str_to_reply = name + ' drank ' + str(amount_drank) + ' coffee out of ' + str(3) + '\nPlease don\'t drink anymore...'
    else:
        str_to_reply = name + ' drank ' + str(amount_drank) + ' coffee out of ' + str(3) + '.'

    str_to_reply += ' ' + smilies[min(amount_drank-1,len(smilies)-1)]
    logging.info('reply: ' + str_to_reply)
    return str_to_reply


def handleCoffee(name, date):
    smilies = [u'\ud83d\ude43',u'\ud83d\ude0f',u'\ud83d\ude31',u'\ud83d\ude21']
    key = getCoffeeKey(name, date)
    queryCoffee = getCoffeeAmount(key)

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


def update_coffee(request_body, params):
    logging.info('Inside updateCoffee...')
    if len(params) != 1 or not myutils.is_number(params[0]):
        logging.info('Params: {}'.format(params))
        return 'Didn\'t fully understand. Should be like: /coffeeupd 2'

    name = myutils.extract_user_first_name(request_body)
    date = myutils.extract_date(request_body)
    amount = int(params[0])

    key = getCoffeeKey(name, date)
    coffeeDrank = CoffeeStore(key=ndb.Key('CoffeeStore', key),timesDrank=amount)
    coffeeDrank.put()

    return '{}, the coffee amount was updated.'.format(name)
    
