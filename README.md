py-mailinator
=============

[![PyPI version](https://badge.fury.io/py/py-mailinator.svg)](http://badge.fury.io/py/py-mailinator)

An python wrapper for the mailinator.com api

##Installation

Install using pip

```
pip install py-mailinator
```

##Commands

Retrieve Inbox
Get your api key at the mailinator [settings](https://www.mailinator.com/settings.jsp) page.

```
from pymaininator.wrapper import Inbox

inbox = Inbox(api_key)
inbox.get()
print inbox.messages
```

##Check Mail

```
mail = inbox.messages[0]
mail.get_message()
print mail.body
```
##Inbox Object
Methods:
* `get()` : retrieves inbox
* `count()`: run after get, gets length of inbox
* `view_subjects()`: run after get. Gets lists of subject lines of inbox

##Message Object
Methods:
* `get_message()`: retrieves full message body and headers

Attributes:
* `id` : message id
* `subject` : message subject line
* `time` : message delivery time
* `seconds_ago` : number of seconds between time of delivery and time of request
* `fromshort` : short from field
* `fromfull`: full from field
* `ip` : ip address the email was sent from
* `been_read` : boolean if messsage has been opened
* `headers` : only available after `get_message()`, shows the message headers
* `body` : only available after `get_message()`, shows message body

