class Commander:
    def __init__(self):
        self.commands = {}

    def add_command(self, cmd, func):
        self.commands[cmd] = func
        
