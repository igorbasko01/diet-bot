import foodstore
import unittest
from commander import Commander
from google.appengine.ext import ndb
import myutils

class TestFoodstore(unittest.TestCase):
    nosegae_datastore_v3 = True
    
    def test_show_list_of_foods(self):
        foodstore.storeListOfFoods("apple,hummus")
        listOfFoods = foodstore.showListOfFoods({})
        print listOfFoods
        assert listOfFoods == "apple,hummus"

    def test_register_command(self):
        cmndr = Commander()
        foodstore.registerFoodStoreCommands(cmndr)
        foodstore.storeListOfFoods("fries")
        listOfFoods = cmndr.execute("/showfoods", {})
        assert listOfFoods == "fries"


    def test_add_food_new(self):
        cmndr = Commander()
        foodstore.registerFoodStoreCommands(cmndr)
        result = cmndr.execute('/addfood', {}, ['h','30'])
        assert result == 'Food h added, calories: 30.'


    def test_add_food_no_params(self):
        cmndr = Commander()
        foodstore.registerFoodStoreCommands(cmndr)
        result = cmndr.execute('/addfood', {})
        assert result == 'Didn\'t fully understand. Should be like: /addfood walnut 30'


    def test_add_food_less_params(self):
        cmndr = Commander()
        foodstore.registerFoodStoreCommands(cmndr)
        result = cmndr.execute('/addfood', 'hello')
        assert result == 'Didn\'t fully understand. Should be like: /addfood walnut 30'


    def test_add_food_more_params(self):
        cmndr = Commander()
        foodstore.registerFoodStoreCommands(cmndr)
        result = cmndr.execute('/addfood', ['hello','dfasd', 'asdfa'])
        assert result == 'Didn\'t fully understand. Should be like: /addfood walnut 30'


    def test_add_food_exists(self):
        cmndr = Commander()
        foodstore.registerFoodStoreCommands(cmndr)
        cmndr.execute('/addfood', {}, ['h','200'])
        result = cmndr.execute('/addfood', {}, ['h','100'])
        assert result == 'Food h already exists...'


    def test_add_food_calories_not_number(self):
        cmndr = Commander()
        foodstore.registerFoodStoreCommands(cmndr)
        result = cmndr.execute('/addfood', {}, ['h','twenty'])
        assert result == 'Invalid calories ! should be a number greater than 0.'


    def test_add_food_emoji(self):
        cmndr = Commander()
        foodstore.registerFoodStoreCommands(cmndr)
        result = cmndr.execute('/addfood', {}, ['\U0001f33d','100'])
        assert result == 'Food \\U0001f33d added, calories: 100.'

    def test_add_default_food(self):
        cmndr = Commander()
        foodstore.registerFoodStoreCommands(cmndr)
        result = cmndr.execute('/add_food_default', {}, ['\ud83c\udf6a','100'])
        assert result == 'Got it ! \ud83c\udf6a=100'

    def test_add_food_user(self):
        cmndr = Commander()
        foodstore.registerFoodStoreCommands(cmndr)
        request_body = {'message': {'from': {u'id': 123}}}
        result = myutils.handle_message(cmndr, u'/add_food', request_body, [u'\ud83c\udf6a',u'100'])
        assert result == [u'Got it ! \ud83c\udf6a=100']
        assert ndb.Key('FoodCalorieValues', u'\ud83c\udf6a:123').get().calories == 100

    def test_show_food_not_recognized(self):
        cmndr = Commander()
        foodstore.registerFoodStoreCommands(cmndr)
        request_body = {'message': {'from': {u'id': 123}}}
        result = myutils.handle_message(cmndr, u'/show_food', request_body, [u'\ud83c\udf6a'])
        assert result == [u'Sorry, I don\'t recognize this food: \ud83c\udf6a']

    def test_show_food(self):
        cmndr = Commander()
        foodstore.registerFoodStoreCommands(cmndr)
        request_body = {'message': {'from': {u'id': 123}}}
        myutils.handle_message(cmndr, u'/add_food', request_body, [u'\ud83c\udf6a', u'100'])
        result = myutils.handle_message(cmndr, u'/show_food', request_body, [u'\ud83c\udf6a'])
        assert result == [u'Custom \ud83c\udf6a = 100']
        myutils.handle_message(cmndr, u'/add_food_default', request_body, [u'\ud83c\udf6a', u'35'])
        result = myutils.handle_message(cmndr, u'/show_food', request_body, [u'\ud83c\udf6a'])
        assert result == [u'Default \ud83c\udf6a = 35\nCustom \ud83c\udf6a = 100']

    def test_show_foods(self):
        cmndr = Commander()
        foodstore.registerFoodStoreCommands(cmndr)
        request_body = {'message': {'from': {u'id': 123}}}
        myutils.handle_message(cmndr, u'/add_food_default', request_body, [u'\ud83c\udf6a', u'100'])
        myutils.handle_message(cmndr, u'/add_food_default', request_body, [u'\ud83c\udf6b', u'100'])
        myutils.handle_message(cmndr, u'/add_food', request_body, [u'\ud83c\udf6b', u'20'])
        result = myutils.handle_message(cmndr, u'/show_foods', request_body, [])
        assert result == [u'Default foods: \n\U0001f36a = 100\n\U0001f36b = 100\nCustom foods: \n\U0001f36b = 20']
        #assert result == [u'Default foods: \n\ud83c\udf6a = 100\n\ud83c\udf6b = 100\nCustom foods: \n\ud83c\udf6b = 20']
