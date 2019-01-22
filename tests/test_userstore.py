import userstore
import unittest
from commander import Commander
from google.appengine.ext import ndb

class TestUserStore(unittest.TestCase):
    nosegae_datastore_v3 = True

    def test_set_max_calories(self):
        userstore.set_max_calories({'message': {'date': 1542830400, 'from': {'first_name': 'igor', 'id':'742'}}}, ['1570'])
        user_obj = ndb.Key('UserStore', '742').get()
        assert user_obj.max_calories == 1570

    def test_reply_max_calories_empty(self):
        reply = userstore.reply_max_calories({'message': {'date': 1542830400, 'from': {'first_name': 'igor', 'id':'742'}}})
        assert reply == 'igor, sorry but you didn\'t set max calories.'

    def test_reply_max_calories(self):
        request = {'message': {'date': 1542830400, 'from': {'first_name': 'igor', 'id':'742'}}}
        userstore.set_max_calories(request, ['1800'])
        reply = userstore.reply_max_calories(request)
        assert reply == 'igor, your max calories is 1800'

    def test_set_max_cal_commander(self):
        cmndr = Commander()
        userstore.register_user_commands(cmndr)
        request_body = {'message': {'from': {'first_name': 'igor', 'id': '777'}}}
        set_reply = cmndr.execute('/set_max_calories', request_body, ['2000'])
        get_reply = cmndr.execute('/show_max_calories', request_body)
        assert set_reply == 'igor, max calories were updated.'
        assert get_reply == 'igor, your max calories is 2000'

    def test_set_max_cal_commander_wrong(self):
        cmndr = Commander()
        userstore.register_user_commands(cmndr)
        request_body = {'message': {'from': {'first_name': 'igor', 'id': '777'}}}
        set_reply = cmndr.execute('/set_max_calories', request_body, [])
        assert set_reply == 'Didn\'t fully understand. Should be like: /set_max_calories 1800'
        set_reply = cmndr.execute('/set_max_calories', request_body, ['fdsd'])
        assert set_reply == 'Didn\'t fully understand. Should be like: /set_max_calories 1800'
        set_reply = cmndr.execute('/set_max_calories', request_body, ['200', '2002'])
        assert set_reply == 'Didn\'t fully understand. Should be like: /set_max_calories 1800'

    def test_reply_max_cal_comndr(self):
        cmndr = Commander()
        userstore.register_user_commands(cmndr)
        request_body = {'message': {'from': {'first_name': 'igor', 'id': '777'}}}
        show_reply = cmndr.execute('/show_max_calories', request_body)
        assert show_reply == 'igor, sorry but you didn\'t set max calories.'
        cmndr.execute('/set_max_calories', request_body, ['4000'])
        show_reply1 = cmndr.execute('/show_max_calories', request_body)
        assert show_reply1 == 'igor, your max calories is 4000'

    def test_reply_max_cal_comndr_wrong(self):
        cmndr = Commander()
        userstore.register_user_commands(cmndr)
        request_body = {'message': {'from': {'first_name': 'igor', 'id': '777'}}}
        show_reply = cmndr.execute('/show_max_calories', request_body, ['hello'])
        assert show_reply == 'igor, sorry but you didn\'t set max calories.'
        set_reply = cmndr.execute('/set_max_calories', request_body, ['2345'])
        show_reply1 = cmndr.execute('/show_max_calories', request_body, ['hello'])
        assert show_reply1 == 'igor, your max calories is 2345'
