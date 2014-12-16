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

```
from pymaininator import Inbox

inbox = Inbox(api_key)
inbox.get()
```

Check Mail


