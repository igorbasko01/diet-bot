import userstore
import unittest
from google.appengine.ext import ndb

class TestUserStore(unittest.TestCase):
    nosegae_datastore_v3 = True

    def test_set_max_calories(self):
        userstore.set_max_calories({'message': {'date': 1542830400, 'from': {'first_name': 'igor', 'id':'742'}}}, ['1570'])
        user_obj = ndb.Key('UserStore', '742').get()
        assert user_obj.max_calories == 1570
