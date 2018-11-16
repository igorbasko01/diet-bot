import unittest
from commander import Commander

class TestCommander(unittest.TestCase):
    def test_register_and_execute(self):
        commander = Commander()
        def command():
            return True
        commander.register_command('command', command)
        result = commander.execute('command')
        assert result == True


    def test_has_command(self):
        cmndr = Commander()
        def command():
            return True
        cmndr.register_command('com', command)
        result_true = cmndr.has_command('com')
        result_false = cmndr.has_command('com_false')
        assert result_true == True
        assert result_false == False
            
