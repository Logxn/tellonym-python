# Unofficial Tellonym SDK for Python
![GitHub Contributors](https://img.shields.io/github/contributors/logxn/tellonym-python.svg)
![GitHub Repo Size](https://img.shields.io/github/repo-size/logxn/tellonym-python.svg)
![GitHub License](https://img.shields.io/github/license/logxn/tellonym-python.svg)

# ⚠️ Warning: This could get you banned
On 1/6/2022 I was banned from using Tellonym.<br>
![Ban Message](https://i.imgur.com/SaHwaZZ.png)<br>
German Text: "You have been blocked from using our services"<br>

So I wrote support and asked them what was going on.<br>
This is the message I received:<br>
![Support Message](https://i.imgur.com/NzxCj42.png)<br>
German Text: "You have used 3rd-Party tools in the past. Your account is now permanently banned."<br>

While creating this API wrapper I might have triggered some sort of bot detection.<br>
But my best bet is that I have left some of my user identification in the code and people who have downloaded and used this wrapper did their stuff 
using my id.<br>
This 'project' never was intended to be used as a bot and I do not want to support creations of different bots.<br>
What people do with this API wrapper shall not be of my concern and I shall not be held responsible for anything others do.<br><br>

Please be careful, I will investigate this and rework the whole wrapper 😌

## Usage
```python
from tellonym import Tellonym as client

client = client.Tellonym(username, password)
profile = client.get_profile()
```

### Client
```python
>>> client.get_tells() # will return an array with tell objects
>>> client.send_tell(user_id, text, anonymous=True)
>>> client.delete_tell(tell_id)
>>> client.get_user() # will return a user object
>>> client.logout()
```

### Profile
```python
>>> profile.is_default_phonenumber()
```

### Answer
```python
>>> answer.is_anonymous_tell()
>>> answer.like()
>>> answer.delete()
```
