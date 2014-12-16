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

    def test_view_subjects(self):
        wrapper.urllib.urlopen = get_mailbox
        inbox = wrapper.Inbox('123')
        inbox.get()
        self.assertEquals(type(inbox.view_subjects()), list)
        self.assertGreater(len(inbox.view_subjects()), 0)

    def test_view_message_ids(self):
        wrapper.urllib.urlopen = get_mailbox
        inbox = wrapper.Inbox('123')
        inbox.get()
        self.assertEquals(type(inbox.view_message_ids()), list)
        self.assertGreater(len(inbox.view_message_ids()), 0)

    def test_get_message_by_subject(self):
        wrapper.urllib.urlopen = get_mailbox
        inbox = wrapper.Inbox('123')
        inbox.get()
        message = inbox.get_message_by_subject('Want to cheat? ')
        self.assertEquals(message.subject, 'Want to cheat? ')


    def test_get_message_by_id(self):
        wrapper.urllib.urlopen = get_mailbox
        inbox = wrapper.Inbox('123')
        inbox.get()
        message = inbox.get_message_by_id('1418740612-3134545-m8r-rmtci4')
        self.assertEquals(message.id, '1418740612-3134545-m8r-rmtci4')


if __name__ == '__main__':
    unittest.main()