import logging

from google.appengine.ext import ndb

import myutils
import userstore
import datetime

# Stores the calories of specific foods.
# The user_id is stored not only as part of a key,
# it is also as part of the entity, so it could be searched.
# Another thing is that deault food calories are stored under
# user_id = 0. But the key is only the food's emoji.
class FoodCalorieValues(ndb.Model):
    user_id = ndb.IntegerProperty()     # 0 Is default
    calories = ndb.IntegerProperty()

# The amount of calories a certain user consumed in a certain day.
class CalorieStore(ndb.Model):
    calories = ndb.IntegerProperty()

def registerFoodStoreCommands(commander):
    commander.register_command('/add_food_default', add_food_default)
    commander.register_command('/add_food', add_food_user)
    commander.register_command('/show_food', show_food)
    commander.register_command('/show_foods', show_foods)
    register_handle_foods(commander)

def register_handle_foods(commander):
    commander.register_command(commander.KEY_OTHER, handle_foods)

def getCaloriesKey(uid, date):
    date_got = datetime.datetime.fromtimestamp(int(date)).strftime("%Y-%m-%d")
    key = '{}:calories:{}'.format(uid, date_got)
    return key

def getCalories(key):
    return ndb.Key('CalorieStore', key).get()

def add_food_default(request_body, params):
    return add_food(request_body, params, is_user=False)

def add_food_user(request_body, params):
    return add_food(request_body, params, is_user=True)
    
def add_food(request_body, params, is_user=False):
    cmd_name = '/add_food_default' if not is_user else '/add_food'
    if len(params) != 2:
        logging.info('Params: {}'.format(params))
        return u'Didn\'t fully understand. Should be like: {} \ud83c\udf6a 100'.format(cmd_name)

    food_name = params[0]
    calories = params[1]
    if not myutils.is_number(calories) or int(calories) < 1:
        return 'Invalid calories ! Should be a number greater than 0.'

    key = food_name + ':' + str(myutils.extract_user_id(request_body)) if is_user else food_name
    user_id = 0 if not is_user else myutils.extract_user_id(request_body)
    food = FoodCalorieValues(key=ndb.Key('FoodCalorieValues',key), calories=int(calories), user_id=user_id)
    food.put()

    return 'Got it ! '+food_name+'={}'.format(calories)


def show_food(request_body, params):
    if len(params) != 1:
        logging.info('Params: {}'.format(params))
        return u'Didn\'t fully understand. Should be like: /show_food \ud83c\udf6a'

    food_name = params[0]
    user_id = str(myutils.extract_user_id(request_body))

    default_cals = ndb.Key('FoodCalorieValues', food_name).get()
    user_cals = ndb.Key('FoodCalorieValues', food_name+':'+user_id).get()

    results = []
    if default_cals is not None:
        results.append(u'Default {} = {}'.format(food_name, default_cals.calories))
    if user_cals is not None:
        results.append(u'Custom {} = {}'.format(food_name, user_cals.calories))

    if len(results) == 0:
        results.append(u'Sorry, I don\'t recognize this food: {}'.format(food_name))

    return '\n'.join(results)

def show_foods(request_body):
    default_foods = get_foods(0)  # get default foods.

    user_id = myutils.extract_user_id(request_body)
    custom_foods = get_foods(user_id)

    default_foods_pretty = ['{} = {}'.format(x[0], x[1]) for x in default_foods.items()]
    custom_foods_pretty = ['{} = {}'.format(x[0], x[1]) for x in custom_foods.items()]
    all_foods = ['Default foods: '] + default_foods_pretty + ['Custom foods: '] + custom_foods_pretty
    result = '\n'.join(all_foods)

    return result.decode('utf-8')

def get_foods(user_id):
    foods = {}
    for food in FoodCalorieValues.query(FoodCalorieValues.user_id==user_id).fetch():
        food_id = food.key.id() if user_id == 0 else food.key.id().split(':')[0]
        foods[food_id] = food.calories

    return foods

def handle_foods(request_body, text):
    uid = myutils.extract_user_id(request_body)
    user_obj = userstore.get_max_calories(uid)

    reply = []
    max_calories = 0
    if user_obj == None:
        reply.append('Sorry, you didn\'t set max calories. Please use /set_max_calories command.')
    else:
        max_calories = user_obj.max_calories

    # Create a dict of foods where the custom foods override the default foods
    # where necessary.
    foods = get_foods(0)
    custom_foods = get_foods(uid)
    for food in custom_foods.items():
        foods[food[0]] = food[1]

    calories_consumed = 0
    food_found = False
    logging.info(foods)
    logging.info(text)
    logging.info(len(text))
    len_text = len(text)
    for i in range(0, len_text):
        check = text[i]
        check_enc = check.encode('utf-8')
        logging.info(check)
        logging.info(check_enc)
        if check_enc in foods or check in foods:
            calories_consumed += foods[check_enc]
            food_found = True
        if i < len_text-1:
            check = text[i]+text[i+1] # if i < len_text-1 else text[i]
            check_enc = check.encode('utf-8')
            logging.info(check)
            logging.info(check_enc)
            if check_enc in foods or check in foods:
                calories_consumed += foods[check_enc]
                food_found = True

    # If no food found, maybe it was only text or not food tracking at all.
    if not food_found:
        return ''

    date = myutils.extract_date(request_body)

    key = getCaloriesKey(uid, date)
    calories_obj = getCalories(key)

    if calories_obj is not None:
        calories_consumed += calories_obj.calories

    update_obj = CalorieStore(key=ndb.Key('CalorieStore', key), calories=calories_consumed)
    update_obj.put()

    reply.append('Calories counted {}/{}'.format(calories_consumed, max_calories))

    return '\n'.join(reply)
