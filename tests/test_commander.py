import unittest
from commander import Commander

class TestCommander(unittest.TestCase):
    def test_register_and_execute(self):
        commander = Commander()
        def command(request_body):
            return True
        commander.register_command('command', command)
        result = commander.execute('command', {})
        assert result == True


    def test_execute_params(self):
        commander = Commander()
        def command(text):
            return text
        commander.register_command('com', command)
        result = commander.execute('com', 'shalom')
        assert result == 'shalom'


    def test_has_command(self):
        cmndr = Commander()
        def command():
            return True
        cmndr.register_command('com', command)
        result_true = cmndr.has_command('com')
        result_false = cmndr.has_command('com_false')
        assert result_true == True
        assert result_false == False

    def test_register_other_command(self):
        cmndr = Commander()
        def other_command_t():
            return True
        def other_command_f():
            return False
        cmndr.register_command(cmndr.KEY_OTHER, other_command_t)
        cmndr.register_command(cmndr.KEY_OTHER, other_command_f)
        assert cmndr.commands[cmndr.KEY_OTHER] == [other_command_t, other_command_f]

    def test_execute_other(self):
        cmndr = Commander()
        def other_command2(r, t):
            return 'command 2'
        def other_command1(r):
            return 'command 1'
        cmndr.register_command(cmndr.KEY_OTHER, other_command1)
        cmndr.register_command(cmndr.KEY_OTHER, other_command2)
        result = cmndr.execute_other('request_body', 'msg text')
        assert result == ['command 1', 'command 2']
            
