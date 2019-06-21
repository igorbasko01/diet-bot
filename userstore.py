from google.appengine.ext import ndb

import logging
import myutils

class UserStore(ndb.Model):
    max_calories = ndb.IntegerProperty()
    join_date = ndb.DateTimeProperty(auto_now_add=True)

def register_user_commands(commander):
    commander.register_command('/set_max_calories', set_max_calories)
    commander.register_command('/show_max_calories', reply_max_calories)
    commander.register_command('/help', help_msg)


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

def get_max_calories(uid):
    return ndb.Key('UserStore', uid).get()

def reply_max_calories(request_body):
    uid = myutils.extract_user_id(request_body)
    name = myutils.extract_user_first_name(request_body)
    user_obj = get_max_calories(uid)
    if user_obj is None:
        return '{}, sorry but you didn\'t set max calories.'.format(name)
    else:
        return '{}, your max calories is {}'.format(name, user_obj.max_calories)

    
def help_msg(request_body):
    name = myutils.extract_user_first_name(request_body)

    return u'''
            Hi {},
            Thanks for choosing me for your calories tracking.
            To log a food that you've eaten, just send \ud83c\udf55 or any
            food that you prefer.
            To track coffee intake, just send \u2615, it also will
            track the calories of the coffee.
            To log water intake, just send \ud83c\udf76.
            And of course all the emojis can be combined in one message.
            To list the caloric value of all available foods to track
            send the /show_foods command.
            To change the caloric value of a food or add another food
            for tracking use the /add_food command.
            There are some more commands, feel free to explore.
            '''.format(name)
    
