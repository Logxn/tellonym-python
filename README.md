# Unofficial Tellonym SDK for Python
![GitHub Contributors](https://img.shields.io/github/contributors/logxn/tellonym-python.svg)
![GitHub Repo Size](https://img.shields.io/github/repo-size/logxn/tellonym-python.svg)
![GitHub License](https://img.shields.io/github/license/logxn/tellonym-python.svg)

A unofficial python module to easily interact with [Tellonym](https://tellonym.me)

## Usage
```python
from tellonym import Tellonym as tell

tell = tell.Tellonym(username, password)
user = tell.get_user()
```

### Client
```python
>>> tell.get_tells() # will return an array with your tells and all its information
>>> tell.send_tell(user_id, text, anonymous=True)
>>> tell.delete_tell(tell_id)
>>> tell.get_user() # will return a user object
>>> tell.logout()
```

### User
```python
>>> user.is_default_phonenumber()
>>> user.get_config() # will return a config object
>>> user.get_answers() # will return an array with answer objects
```

### Answer
```python 
>>> answer.is_anonymous_tell()
```
