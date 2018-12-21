from google.appengine.ext import ndb

import logging
import myutils
import logging

class UserStore(ndb.Model):
    max_calories = ndb.IntegerProperty()

def register_user_commands(commander):
    commander.register_command('/set_max_calories', set_max_calories)
    commander.register_command('/show_max_calories', get_max_calories)


def set_max_calories(request_body, params):
    if len(params) != 1 or not myutils.is_number(params[0]):
        logging.info('Params: {}'.format(params))
        return 'Didn\'t fully understand. Should be like: /set_max_calories 1800'

    uid = myutils.extract_user_id(request_body)
    name = myutils.extract_user_first_name(request_body)
    new_calories = int(params[0])
    logging.info('uid: {}, cals: {}'.format(uid, new_calories))

    user_obj = UserStore(key=ndb.Key('UserStore', uid), max_calories=new_calories)
    user_obj.put()

    return '{}, max calories were updated.'.format(name)

def get_max_calories(request_body):
    uid = myutils.extract_user_id(request_body)
    name = myutils.extract_user_first_name(request_body)
    user_obj = ndb.Key('UserStore', uid).get()
    if user_obj is None:
        return '{}, sorry but you didn\'t set max calories.'.format(name)
    else:
        return '{}, your max calories is {}'.format(name, user_obj.max_calories)
    
