# Unofficial Tellonym SDK for Python
A unofficial python module to easily interact with [Tellonym](https://tellonym.me)

## Usage
```python
from tellonym import Tellonym as tell

tell = tell.Tellonym(username, password)
```

### Tells
```python
>>> tell.delete_tell(tell_id)
```

### Misc
```python
>>> tell.logout()
```
