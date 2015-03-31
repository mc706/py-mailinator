import unittest
import os
from pymailinator import wrapper


class MockResponse(object):
    def __init__(self, url=None, content=None, status=None, filename=None):
        self.content = content
        self.status = status
        self.url = url
        if filename and not content:
            with open(filename, 'r') as f:
                self.content = f.read()

    def getcode(self):
        return self.status

    def read(self):
        return self.content


def get_empty_mailbox(url):
    return MockResponse(status=200, content='{"messages":[]}', url=url)


def get_bad_api_token(url):
    return MockResponse(status=400, content='', url=url)


def get_missing_token(url):
    return MockResponse(status=404, url=url)


def get_missing_message(url):
    return MockResponse(status=404, url=url)


def get_mailbox(url):
    filename = os.path.join(os.path.dirname(__file__), 'json', 'mailbox.json')
    return MockResponse(status=200, filename=filename, url=url)


def get_message(url):
    filename = os.path.join(os.path.dirname(__file__), 'json', 'message.json')
    return MockResponse(status=200, filename=filename, url=url)


# noinspection PyArgumentList
class TestWrapper(unittest.TestCase):
    def test_empty_mailbox(self):
        wrapper.urlopen = get_empty_mailbox
        inbox = wrapper.Inbox('123')
        inbox.get()
        self.assertEqual(inbox.count(), 0)
        self.assertEquals(inbox.messages, [])

    def test_bad_token(self):
        wrapper.urlopen = get_bad_api_token
        inbox = wrapper.Inbox('123')
        with self.assertRaises(wrapper.InvalidToken):
            inbox.get()

    def test_missing_token(self):
        with self.assertRaises(TypeError):
            wrapper.Inbox()

    def test_invalid_token(self):
        wrapper.urlopen = get_missing_token
        inbox = wrapper.Inbox(False)
        with self.assertRaises(wrapper.MissingToken):
            inbox.get()

    def test_successful_mailbox(self):
        wrapper.urlopen = get_mailbox
        inbox = wrapper.Inbox('123')
        inbox.get()
        self.assertGreater(inbox.count(), 0)

    def test_successful_message(self):
        wrapper.urlopen = get_mailbox
        inbox = wrapper.Inbox('123')
        inbox.get()
        wrapper.urlopen = get_message
        message = inbox.messages[0]
        message.get_message()
        self.assertNotEquals(message.body, '')

    def test_missing_message(self):
        wrapper.urlopen = get_mailbox
        inbox = wrapper.Inbox('123')
        inbox.get()
        wrapper.urlopen = get_missing_message
        with self.assertRaises(wrapper.MessageNotFound):
            inbox.messages[0].get_message()

    def test_view_subjects(self):
        wrapper.urlopen = get_mailbox
        inbox = wrapper.Inbox('123')
        inbox.get()
        self.assertEquals(type(inbox.view_subjects()), list)
        self.assertGreater(len(inbox.view_subjects()), 0)

    def test_view_message_ids(self):
        wrapper.urlopen = get_mailbox
        inbox = wrapper.Inbox('123')
        inbox.get()
        self.assertEquals(type(inbox.view_message_ids()), list)
        self.assertGreater(len(inbox.view_message_ids()), 0)

    def test_get_message_by_subject(self):
        wrapper.urlopen = get_mailbox
        inbox = wrapper.Inbox('123')
        inbox.get()
        message = inbox.get_message_by_subject('Want to cheat? ')
        self.assertEquals(message.subject, 'Want to cheat? ')

    def test_get_message_by_id(self):
        wrapper.urlopen = get_mailbox
        inbox = wrapper.Inbox('123')
        inbox.get()
        message = inbox.get_message_by_id('1418740612-3134545-m8r-rmtci4')
        self.assertEquals(message.id, '1418740612-3134545-m8r-rmtci4')

    def test_filter_inbox(self):
        wrapper.urlopen = get_mailbox
        inbox = wrapper.Inbox('123')
        inbox.get()
        filtered_me = inbox.filter('to', 'me')
        self.assertEquals(len(filtered_me), 0)
        filtered = inbox.filter('to', 'm8r-rmtci4@mailinator.com')
        self.assertEquals(len(filtered), 2)

    def test_other_mailbox(self):
        wrapper.urlopen = get_mailbox
        inbox = wrapper.Inbox('123')
        inbox.get('other')
        self.assertGreater(inbox.count(), 0)


if __name__ == '__main__':
    unittest.main()