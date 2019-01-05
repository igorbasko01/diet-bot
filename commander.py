import logging

class Commander:
    KEY_OTHER = 'OTHER'
    
    def __init__(self):
        self.commands = {}
        self.commands[self.KEY_OTHER] = []

    def register_other_command(self, func):
        other_funcs = self.commands[self.KEY_OTHER]
        other_funcs += [func]
        self.commands[self.KEY_OTHER] = other_funcs
        

    def register_command(self, cmd, func):
        #TODO: Don't allow to register existing key.
        if cmd == self.KEY_OTHER:
            self.register_other_command(func)
        else:
            self.commands[cmd] = func

    def has_command(self, cmd):
        return True if cmd in self.commands else False

    def execute(self, cmd, request_body, params=[]):
        logging.info('Going to execute the following command: ' + cmd)
        logging.info(request_body)
        logging.info(params)
        try:
            return self.commands[cmd](request_body, params)
        except KeyError, e:
            logging.info('Couldn\'t find the following registered command: ' % str(cmd))
        except TypeError, e:
            print(e)
            return self.commands[cmd](request_body)

    def execute_other(self, request_body, text):
        other_funcs = self.commands[self.KEY_OTHER]
        replies = []
        for func in other_funcs:
            try:
                reply = func(request_body, text)
            except TypeError, e:
                reply = func(request_body)
            replies += [reply]
        return replies
