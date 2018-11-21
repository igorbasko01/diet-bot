from google.appengine.ext import ndb

import logging
import datetime

class CoffeeStore(ndb.Model):
    timesDrank = ndb.IntegerProperty()


def registerCoffeeCommands(commander):
    commander.register_command('/coffeeupd', update_coffee)

def getCoffeeKey(name, date):
    date_got = datetime.datetime.fromtimestamp(int(date)).strftime("%Y-%m-%d")
    key = '{}:coffee:{}'.format(name, date_got)
    return key

def getCoffeeAmount(key):
    return ndb.Key('CoffeeStore', key).get()

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


def update_coffee(params):
    logging.info('Inside updateCoffee...')
    if len(params) != 3:
        logging.info('Params: {}'.format(params))
        return 'Didn\'t fully understand. Should be like: /coffeeupd 2'

    name = params[0]
    date = params[1]
    amount = params[2]

    key = getCoffeeKey(name, date)
    coffeeDrank = CoffeeStore(key=ndb.Key('CoffeeStore', key),timesDrank=amount)
    coffeeDrank.put()

    return '{}, the coffee amount was updated.'.format(name)
    
