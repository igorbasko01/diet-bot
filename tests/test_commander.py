import pytest
from commander import Commander

class TestCommander(object):
    def test_register_and_execute(self):
        commander = Commander()
        def command():
            return True
        commander.register_command('command', command)
        result = commander.execute('command')
        assert result == True
