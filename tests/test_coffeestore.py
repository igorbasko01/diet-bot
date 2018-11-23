import coffeestore
import unittest
from commander import Commander
from google.appengine.ext import ndb

class TestCoffeestore(unittest.TestCase):
    nosegae_datastore_v3 = True

    def test_get_coffee_key(self):
        key = coffeestore.getCoffeeKey('igor', '1542830400')
        assert key == 'igor:coffee:2018-11-21'

    def test_get_coffee_amount(self):
        key = coffeestore.getCoffeeKey('igor', '1542830400')
        coffeeDrank = coffeestore.CoffeeStore(key=ndb.Key('CoffeeStore', key),timesDrank=3)
        coffeeDrank.put()
        coffeeResult = coffeestore.getCoffeeAmount(key)
        assert coffeeResult.timesDrank == 3

    def test_handle_coffee(self):
        coffeeDrank = coffeestore.handleCoffee('igor', '1542830400')
        assert u'igor drank 1 coffee out of 3.' in coffeeDrank


    def test_update_coffee(self):
        cmndr = Commander()
        coffeestore.registerCoffeeCommands(cmndr)
        cmndr.execute('/coffeeupd', {'message': {'date': 1542830400, 'from': {'first_name': 'igor'}}}, ['10'])
        key = coffeestore.getCoffeeKey('igor', '1542830400')
        coffee_amount = coffeestore.getCoffeeAmount(key)
        assert coffee_amount.timesDrank == 10
        
