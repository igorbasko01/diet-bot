from google.appengine.ext import ndb

import userstore
import myutils

class EnableStatus(ndb.Model):
    # key name: str(chat_id)
    enabled = ndb.BooleanProperty(indexed=False, default=False)


def register_user_commands(commander):
    commander.register_command('/start', enable_bot)
    commander.register_command('/stop', disable_bot)


def setEnabled(chat_id, yes):
    es = EnableStatus.get_or_insert(str(chat_id))
    es.enabled = yes
    es.put()

def getEnabled(chat_id):
    es = EnableStatus.get_by_id(str(chat_id))
    if es:
        return es.enabled
    return False


def enable_bot(request_body):
    chat_id = myutils.extract_chat_id(request_body)
    setEnabled(chat_id, True)
    return userstore.help_msg(request_body)


def disable_bot(request_body):
    chat_id = myutils.extract_chat_id(request_body)
    setEnabled(chat_id, False)
    return 'Bye Bye'
