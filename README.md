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
from pymaininator import Inbox

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


##Message Object

