import logging

from google.appengine.ext import ndb

import myutils

# Stores a list of different foods that the user configured.
# Used as an index, to know which foods exists in the system.
class FoodsListStore(ndb.Model):
    listOfNames = ndb.StringProperty()

class FoodCalorieValues(ndb.Model):
    user_id = ndb.IntegerProperty()     # 0 Is default
    calories = ndb.IntegerProperty()

def registerFoodStoreCommands(commander):
    commander.register_command('/showfoods', showListOfFoods)
    commander.register_command('/addfood', addFood)
    commander.register_command('/add_food_default', add_food_default)
    commander.register_command('/add_food', add_food_user)
    commander.register_command('/show_food', show_food)
    commander.register_command('/show_foods', show_foods)

def getListOfFoods():
    return ndb.Key('FoodsListStore', 'FoodsList').get()

def storeListOfFoods(foodsToStore):
    foodsList = FoodsListStore(key=ndb.Key('FoodsListStore', 'FoodsList'),listOfNames=foodsToStore)
    foodsList.put()

def showListOfFoods(request_body):
    queryFoodList = getListOfFoods()
    foodList = 'No foods !'
    if queryFoodList is not None:
        foodList = queryFoodList.listOfNames
    return foodList

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
    default_foods = [
        (x.key.id(), x.calories) for x in
        FoodCalorieValues.query(FoodCalorieValues.user_id==0).fetch()
    ]

    user_id = myutils.extract_user_id(request_body)
    custom_foods = [
        (x.key.id().split(':')[0], x.calories) for x in
        FoodCalorieValues.query(FoodCalorieValues.user_id==user_id).fetch()
    ]
    default_foods_pretty = ['{} = {}'.format(x[0], x[1]) for x in default_foods]
    custom_foods_pretty = ['{} = {}'.format(x[0], x[1]) for x in custom_foods]
    all_foods = ['Default foods: '] + default_foods_pretty + ['Custom foods: '] + custom_foods_pretty
    
    return '\n'.join(all_foods)

def addFood(request_body, params):
    if len(params) != 2:
        logging.info('Params: {}'.format(params))
        return 'Didn\'t fully understand. Should be like: /addfood walnut 30'

    foodName = params[0]
    calories = params[1]
    if not myutils.is_number(calories) or int(calories) < 1:
        return 'Invalid calories ! should be a number greater than 0.'

    result_msg = ''

    # Get list of food names.
    queryFoodList = getListOfFoods()
    foodsListArray = []
    if queryFoodList is not None:
        foodsListArray = queryFoodList.listOfNames.split(',')
    logging.info('Got food list: ' + str(foodsListArray))

    # add the new food only if its not already in the list.
    if foodName not in foodsListArray:
        foodsListArray.append(foodName)
        foodsListString = ",".join(foodsListArray)
        storeListOfFoods(foodsListString)
        result_msg = 'Food ' + foodName + ' added, calories: ' + str(calories) + '.'
    else:
        result_msg = 'Food ' + foodName + ' already exists...'

    return result_msg
