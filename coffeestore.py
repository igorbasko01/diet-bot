from google.appengine.ext import ndb

import logging
import datetime

class CoffeeStore(ndb.Model):
    timesDrank = ndb.IntegerProperty()


def registerCoffeCommands(commander):
    commander.register_command('/coffeeupd', new_update_coffee)

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


# Deprecated
# Need to delete when the new_update_coffee will be ready.
def updateCoffee(name, date, amount):
    date_got = datetime.datetime.fromtimestamp(int(date)).strftime("%Y-%m-%d")
    key = '' + name + ':coffee:' + date_got

    coffeeDrank = CoffeeStore(key=ndb.Key('CoffeeStore', key),timesDrank=amount)
    coffeeDrank.put()

def new_update_coffee(params):
    logging.info('Inside updateCoffee...')
    
