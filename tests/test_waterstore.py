import waterstore
import unittest
from commander import Commander
from google.appengine.ext import ndb

class TestWaterstore(unittest.TestCase):
    nosegae_datastore_v3 = True

    def test_get_water_key(self):
        key = waterstore.getWaterKey('123', '1542830400')
        assert key == '123:water:2018-11-21'

    def test_get_water_amount(self):
        key = waterstore.getWaterKey('123', '1542830400')
        waterDrank = waterstore.WaterStore(key=ndb.Key('WaterStore', key),timesDrank=3)
        waterDrank.put()
        waterResult = waterstore.getWaterAmount(key)
        assert waterResult.timesDrank == 3

    def test_handle_water(self):
        request_body = {'message': {'date': 1542830400, 'from': {'first_name': 'igor', 'id': '123'}}}
        waterDrank = waterstore.handle_water(request_body, u'\U0001f376')
        assert u'Water drank today: 1 cups' in waterDrank

    def test_handle_water_multiple_in_msg(self):
        request_body = {'message': {'date': 1542830400, 'from': {'first_name': 'igor', 'id': '123'}}}
        waterDrank = waterstore.handle_water(request_body, u'\U0001f376 igor ba \U0001f376')
        assert u'Water drank today: 2 cups' in waterDrank

    def test_handle_water_multiple_msgs(self):
        request_body = {'message': {'date': 1542830400, 'from': {'first_name': 'igor', 'id': '123'}}}
        waterDrank = waterstore.handle_water(request_body, u'igor ba \U0001f376')
        waterDrank = waterstore.handle_water(request_body, u' \U0001f376 ba')
        assert u'Water drank today: 2 cups' in waterDrank


    def test_update_water(self):
        cmndr = Commander()
        waterstore.registerWaterCommands(cmndr)
        cmndr.execute('/waterupd', {'message': {'date': 1542830400, 'from': {'first_name': 'igor', 'id': '123'}}}, ['10'])
        key = waterstore.getWaterKey('123', '1542830400')
        water_amount = waterstore.getWaterAmount(key)
        assert water_amount.timesDrank == 10
        
