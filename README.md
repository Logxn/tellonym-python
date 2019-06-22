# Unofficial Tellonym SDK for Python
![GitHub Contributors](https://img.shields.io/github/contributors/logxn/tellonym-python.svg)
![GitHub Repo Size](https://img.shields.io/github/repo-size/logxn/tellonym-python.svg)
![GitHub License](https://img.shields.io/github/license/logxn/tellonym-python.svg)

A unofficial python module to easily interact with [Tellonym](https://tellonym.me)

## Usage
```python
from tellonym import Tellonym as client

client = client.Tellonym(username, password)
user = client.get_user()
```

### Client
```python
>>> client.get_tells() # will return an array with tell objects
>>> client.send_tell(user_id, text, anonymous=True)
>>> client.delete_tell(tell_id)
>>> client.get_user() # will return a user object
>>> client.logout()
```

### User
```python
>>> user.is_default_phonenumber()
```

### Answer
```python
>>> answer.is_anonymous_tell()
>>> answer.like()
>>> answer.delete()
```
