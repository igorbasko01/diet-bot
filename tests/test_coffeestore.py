import coffeestore
import unittest
from commander import Commander
from google.appengine.ext import ndb

class TestCoffeestore(unittest.TestCase):
    nosegae_datastore_v3 = True

    def test_get_coffee_key(self):
        key = coffeestore.getCoffeeKey(123, '1542830400')
        assert key == '123:coffee:2018-11-21'

    def test_get_coffee_amount(self):
        key = coffeestore.getCoffeeKey(123, '1542830400')
        coffeeDrank = coffeestore.CoffeeStore(key=ndb.Key('CoffeeStore', key),timesDrank=3)
        coffeeDrank.put()
        coffeeResult = coffeestore.getCoffeeAmount(key)
        assert coffeeResult.timesDrank == 3

    def test_handle_coffee(self):
        request_body = {'message': {'date': 1542830400, 'from': {'first_name': 'igor'}}}
        coffeeDrank = coffeestore.handle_coffee(request_body, u'\u2615\ufe0f')
        assert u'igor drank 1 coffee out of 3.' in coffeeDrank

    def test_handle_coffee_multiple_in_msg(self):
        request_body = {'message': {'date': 1542830400, 'from': {'first_name': 'igor'}}}
        coffeeDrank = coffeestore.handle_coffee(request_body, u'\u2615\ufe0f igor ba \u2615\ufe0f')
        assert u'igor drank 2 coffee out of 3.' in coffeeDrank

    def test_handle_coffee_multiple_msgs(self):
        request_body = {'message': {'date': 1542830400, 'from': {'first_name': 'igor'}}}
        coffeeDrank = coffeestore.handle_coffee(request_body, u'igor ba \u2615\ufe0f')
        coffeeDrank = coffeestore.handle_coffee(request_body, u' \u2615\ufe0f ba')
        assert u'igor drank 2 coffee out of 3.' in coffeeDrank


    def test_update_coffee(self):
        cmndr = Commander()
        coffeestore.registerCoffeeCommands(cmndr)
        cmndr.execute('/coffeeupd', {'message': {'date': 1542830400, 'from': {'first_name': 'igor', 'id': 123}}}, ['10'])
        key = coffeestore.getCoffeeKey(123, '1542830400')
        coffee_amount = coffeestore.getCoffeeAmount(key)
        assert coffee_amount.timesDrank == 10
        
