import logging

from google.appengine.ext import ndb

import myutils

# Stores a list of different foods that the user configured.
# Used as an index, to know which foods exists in the system.
class FoodsListStore(ndb.Model):
    listOfNames = ndb.StringProperty()

def showListOfFoods():
    queryFoodList = ndb.Key('FoodsListStore', 'FoodsList').get()
    foodList = 'No foods !'
    if queryFoodList is not None:
        foodList = queryFoodList.listOfNames
    return foodList

def addFood(foodName, calories):
    if not myutils.is_number(calories) or int(calories) < 1:
        return 'Invalid calories ! should be a number greater than 0.'

    result_msg = ''

    # Get list of food names.
    queryFoodList = ndb.Key('FoodsListStore', 'FoodsList').get()
    foodsListArray = []
    if queryFoodList is not None:
        foodsListArray = queryFoodList.listOfNames.split(',')
    logging.info('Got food list: ' + str(foodsListArray))

    # add the new food only if its not already in the list.
    if foodName not in foodsListArray:
        foodsListArray.append(foodName)
        foodsListString = ",".join(foodsListArray)
        foodsList = FoodsListStore(key=ndb.Key('FoodsListStore', 'FoodsList'),listOfNames=foodsListString)
        foodsList.put()
        result_msg = 'Food ' + foodName + ' added, calories: ' + str(calories) + '.'
    else:
        result_msg = 'Food ' + foodName + ' already exists...'

    return result_msg