import unittest
from pymailinator import wrapper


class MockResponse():
    def __init__(self, content=None, status=None, filename=None):
        self.content = content
        self.status = status
        if filename and not content:
            with open(filename, 'r') as f:
                self.content = f.read()

    def getcode(self):
        return self.status

    def read(self):
        return self.content


def get_empty_mailbox(url):
    return MockResponse(status=200, content='{"messages":[]}')


def get_bad_api_token(url):
    return MockResponse(status=400, content='')


def get_missing_message(url):
    return MockResponse(status=404)


def get_mailbox(url):
    return MockResponse(status=200, filename='json/mailbox.json')


def get_message(url):
    return MockResponse(status=200, filename='json/message.json')


class test_wrapper(unittest.TestCase):
    def test_empty_mailbox(self):
        wrapper.urllib.urlopen = get_empty_mailbox
        inbox = wrapper.Inbox('123')
        inbox.get()
        self.assertEqual(inbox.count(), 0)
        self.assertEquals(inbox.messages, [])

    def test_bad_token(self):
        wrapper.urllib.urlopen = get_bad_api_token
        inbox = wrapper.Inbox('123')
        with self.assertRaises(wrapper.InvalidToken):
            inbox.get()

    def test_missing_token(self):
        with self.assertRaises(TypeError):
            wrapper.Inbox()

    def test_successful_mailbox(self):
        wrapper.urllib.urlopen = get_mailbox
        inbox = wrapper.Inbox('123')
        inbox.get()
        self.assertGreater(inbox.count(), 0)

    def test_successful_message(self):
        wrapper.urllib.urlopen = get_mailbox
        inbox = wrapper.Inbox('123')
        inbox.get()
        wrapper.urllib.urlopen = get_message
        message = inbox.messages[0]
        message.get_message()
        self.assertNotEquals(message.body, '')


if __name__ == '__main__':
    unittest.main()