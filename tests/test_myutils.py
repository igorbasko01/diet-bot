import unittest
import myutils

class TestMyutils(unittest.TestCase):
    def test_split_text(self):
        text = "/hello  igor     basko"
        cmd, params = myutils.split_text(text)
        assert cmd == '/hello'
        assert params == ['igor','basko']


    def test_split_text_emoji(self):
        text = u'/addfood \U0001f33d 100'
        cmd, params = myutils.split_text(text)
        assert cmd == u'/addfood'
        assert params == [u'\U0001f33d',u'100']


    def test_logging_info_uni(self):
        myutils.logging_info('Cmd: {}, Params: {}', u'hello', u'\U0001f33d')


    def test_logging_info_simple(self):
        myutils.logging_info('Hello')
