import unittest
import myutils

class TestMyutils(unittest.TestCase):
    def test_split_text(self):
        text = "/hello  igor     basko"
        cmd, params = myutils.split_text(text)
        assert cmd == '/hello'
        assert params == ['igor','basko']
