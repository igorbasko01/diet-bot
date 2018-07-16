import logging

from google.appengine.ext import ndb

class BotToken(ndb.Model):
    token = ndb.StringProperty();
    
def get_token():
    queriedToken = ndb.Key('BotToken', 'dietbottoken').get()
    tokenMessage = 'No token was found !'
    if queriedToken is not None:
        tokenMessage = 'Token Found !'
    logging.info(tokenMessage)
    return queriedToken.token