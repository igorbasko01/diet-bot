import logging

class Commander:
    def __init__(self):
        self.commands = {}

    def register_command(self, cmd, func):
        #TODO: Don't allow to register existing key.
        self.commands[cmd] = func

    def execute(self, cmd):
        logging.info('Going to execute the following command: ' + cmd)
        try:
            return self.commands[cmd]()
        except KeyError, e:
            logging.info('Couldn\'t find the following registered command: ' % str(cmd))
        
