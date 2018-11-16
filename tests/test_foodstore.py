import foodstore
import unittest
from commander import Commander

class TestFoodstore(unittest.TestCase):
    nosegae_datastore_v3 = True
    
    def test_show_list_of_foods(self):
        foodstore.storeListOfFoods("apple,hummus")
        listOfFoods = foodstore.showListOfFoods()
        print listOfFoods
        assert listOfFoods == "apple,hummus"

    def test_register_command(self):
        cmndr = Commander()
        foodstore.registerFoodStoreCommands(cmndr)
        foodstore.storeListOfFoods("fries")
        listOfFoods = cmndr.execute("/showfoods")
        assert listOfFoods == "fries"
