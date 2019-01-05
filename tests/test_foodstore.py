import foodstore
import unittest
from commander import Commander
from google.appengine.ext import ndb

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
        request_body = {'message': {'from': {'id': '123'}}}
        result = cmndr.execute('/add_food', request_body, ['\ud83c\udf6a','100'])
        assert result == 'Got it ! \ud83c\udf6a=100'
        assert ndb.Key('FoodCalorieValues', '\ud83c\udf6a:123').get().calories == 100
