import botenabler
import unittest
from commander import Commander


class TestBotenabler(unittest.TestCase):
    nosegae_datastore_v3 = True

    def test_enable_bot(self):
        cmndr = Commander()
        botenabler.register_user_commands(cmndr)
        request_body = {'message': {'chat': {'id': 123}, 'from': {'first_name': 'Jon'}}}
        result = cmndr.execute('/start', request_body, [])
        assert u'Hi Jon' in result


    def test_disable_bot(self):
        cmndr = Commander()
        botenabler.register_user_commands(cmndr)
        request_body = {'message': {'chat': {'id': 123}, 'from': {'first_name': 'Doe'}}}
        result = cmndr.execute('/stop', request_body, [])
        assert u'Bye Bye' in result

