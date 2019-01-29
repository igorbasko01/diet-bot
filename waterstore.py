from google.appengine.ext import ndb

import logging
import datetime
import myutils

class WaterStore(ndb.Model):
    timesDrank = ndb.IntegerProperty()


def registerWaterCommands(commander):
    commander.register_command('/waterupd', update_water)
    commander.register_command(commander.KEY_OTHER, handle_water)

def getWaterKey(uid, date):
    date_got = datetime.datetime.fromtimestamp(int(date)).strftime("%Y-%m-%d")
    key = '{}:water:{}'.format(uid, date_got)
    return key

def getWaterAmount(key):
    return ndb.Key('WaterStore', key).get()


def handle_water(request_body, text):
    waters = text.count(u'\U0001f376')
    if waters == 0:
        return ''

    uid = myutils.extract_user_id(request_body)
    date = myutils.extract_date(request_body)

    key = getWaterKey(uid, date)
    queryWater = getWaterAmount(key)

    logging.info('key: ' + key)
    logging.info('queryWater.timesDrank: ' + str(queryWater))
    logging.info('Waters to add: {}'.format(waters))

    amount_drank = waters
    if queryWater is not None:
        amount_drank += queryWater.timesDrank

    waterDrank = WaterStore(key=ndb.Key('WaterStore', key),timesDrank=amount_drank)
    waterDrank.put()

    return 'Water drank today: {} cups'.format(amount_drank)


def update_water(request_body, params):
    logging.info('Inside update_water...')
    if len(params) != 1 or not myutils.is_number(params[0]):
        logging.info('Params: {}'.format(params))
        return 'Didn\'t fully understand. Should be like: /waterupd 2'

    name = myutils.extract_user_first_name(request_body)
    uid = myutils.extract_user_id(request_body)
    date = myutils.extract_date(request_body)
    amount = int(params[0])

    key = getWaterKey(uid, date)
    waterDrank = WaterStore(key=ndb.Key('WaterStore', key),timesDrank=amount)
    waterDrank.put()

    return '{}, the water amount was updated.'.format(name)
    
