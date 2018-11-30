import unittest
import myutils
from commander import Commander
import coffeestore

class TestMyutils(unittest.TestCase):
    nosegae_datastore_v3 = True
    
    def test_split_text(self):
        text = "/hello  igor     basko"
        cmd, params = myutils.split_text(text)
        assert cmd == '/hello'
        assert params == ['igor','basko']


    def test_split_text_emoji(self):
        text = u'/addfood \U0001f33d 100'
        cmd, params = myutils.split_text(text)
        assert cmd == u'/addfood'
        assert params == [u'\U0001f33d',u'100']

    def test_handle_message_other(self):
        cmndr = Commander()
        coffeestore.registerCoffeeCommands(cmndr)
        cmd, params = myutils.split_text(u'\u2615\ufe0f \u2615\ufe0f')
        replies = myutils.handle_message(cmndr, cmd, {'message': {'date': 1542830400, 'from': {'first_name': 'igor'}}}, params)
        assert 'igor drank 2 coffee out of 3' in replies[0]

    def test_handle_message_specific(self):
        cmndr = Commander()
        coffeestore.registerCoffeeCommands(cmndr)
        cmd, params = myutils.split_text(u'/coffeeupd 2')
        replies = myutils.handle_message(cmndr, cmd, {'message': {'date': 1542830400, 'from': {'first_name': 'igor'}}}, params)
        assert replies[0] == 'igor, the coffee amount was updated.'
        
