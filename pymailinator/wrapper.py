import json

try:
    from urllib.request import urlopen
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlopen, urlencode


class InvalidToken(Exception):
    pass


class MissingToken(Exception):
    pass


class MessageNotFound(Exception):
    pass


class Message(object):
    """Message Object for Mailinator Email API
    """
    _baseURL = 'http://api.mailinator.com/api/email'

    def __init__(self, token, data):
        self.token = token
        self.id = data['id']
        self.subject = data['subject']
        self.time = data['time']
        self.to = data['to']
        self.seconds_ago = data['seconds_ago']
        self.fromfull = data['fromfull']
        self.been_read = data['been_read']
        self.fromshort = data['from']
        self.ip = data['ip']
        self.headers = {}
        self.body = ""

    def get_message(self):
        query_string = {'token': self.token, 'msgid': self.id}
        url = self._baseURL + "?" + urlencode(query_string)
        request = urlopen(url)
        if request.getcode() == 404:
            raise MessageNotFound
        response = request.read()
        data = json.loads(clean_response(response), strict=False)
        self.headers = data['data']['headers']
        self.body = "".join([part['body'] for part in data['data']['parts']])


class Inbox(object):
    """Inbox Object for retrieving an inbox

    Args:
        token: An api token, from http://www.mailinator.com/settings.jsp
    Methods:
        get:
            Args:
                mailbox: optional argument for the name of an inbox
    Returns:

    Raises:
        InvalidToken: When the api token is invalid
        MissingToken: When run without a token

    """
    _baseURL = "http://api.mailinator.com/api/inbox"

    def __init__(self, token):
        self.token = token
        self.messages = []

    def get(self, mailbox=None, private_domain=False):
        """Retrieves email from inbox"""
        if not self.token:
            raise MissingToken
        query_string = {'token': self.token}
        if mailbox:
            query_string.update({'to': mailbox})
        if private_domain:
            query_string.update({'private_domain': json.dumps(private_domain)})
        url = self._baseURL + '?' + urlencode(query_string)
        request = urlopen(url)
        if request.getcode() == 400:
            raise InvalidToken
        response = request.read()
        return self._parse(response)

    def count(self):
        """returns the number of emails in inbox"""
        return len(self.messages)

    def view_subjects(self):
        """returns a list of messages subjects"""
        return [message.subject for message in self.messages]

    def view_message_ids(self):
        """returns a list of message ids"""
        return [message.id for message in self.messages]

    def get_message_by_subject(self, subject):
        """returns a message object with a subject line"""
        messages = [message for message in self.messages if message.subject.lower() == subject.lower()]
        if len(messages) == 0:
            return None
        elif len(messages) == 1:
            return messages[0]
        else:
            return messages

    def get_message_by_id(self, msgid):
        """returns a message object by id"""
        messages = [message for message in self.messages if message.id == msgid]
        if len(messages) == 0:
            return None
        elif len(messages) == 1:
            return messages[0]

    def filter(self, field, value):
        """returns a filtered list of messages by where message.field = value"""
        return [message for message in self.messages if getattr(message, field) == value]

    def _parse(self, data):
        self.messages = []
        parsed = json.loads(clean_response(data), strict=False)
        for message in parsed['messages']:
            email = Message(self.token, message)
            self.messages.append(email)
        return self.messages


def clean_response(response):
    if not isinstance(response, str):
        return response.decode('utf-8', 'ignore')
    else:
        return response

