import foodstore
import unittest

class TestFoodstore(unittest.TestCase):
    nosegae_datastore_v3 = True
    
    def test_show_list_of_foods(self):
        foodstore.storeListOfFoods("apple,hummus")
        listOfFoods = foodstore.showListOfFoods()
        print listOfFoods
        assert listOfFoods == "apple,hummus"
