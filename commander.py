import logging

class Commander:
    def __init__(self):
        self.commands = {}

    def register_command(self, cmd, func):
        #TODO: Don't allow to register existing key.
        self.commands[cmd] = func

    def has_command(self, cmd):
        return True if cmd in self.commands else False

    def execute(self, cmd, params=''):
        logging.info('Going to execute the following command: ' + cmd)
        try:
            return self.commands[cmd](params)
        except KeyError, e:
            logging.info('Couldn\'t find the following registered command: ' % str(cmd))
        except TypeError, e:
            return self.commands[cmd]()
        
