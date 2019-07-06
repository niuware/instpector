# Instpector

Simple Instagram web API library written in Python 3. Just login with your web user and password and start using. No selenium or webdriver required.

# Installation

```
pip install instpector
```

# Sample usage

```python
from instpector import Instpector

instpector = Instpector()

# Login into Instagram's web
if not instpector.login("my_username", "my_password"):
    return

# Get the profile of any user, for example 'some_username'
profile = instpector.profile()
insta_profile = profile.get_for("some_username")
print(insta_profile)
# id, followers_count, following_count, is_private, ... 

# Iterate all followers of 'some_username'
followers = instpector.followers()
for follower in followers.get_all_for(insta_profile.id):
    print(follower)
    # id, username, full_name, ...
```

Check more details in the `examples` directory.

# Available endpoints

- Followers   
- Following   
- Timeline   
- Profile   

More to come

# Disclaimer

This tool is not affiliated with, authorized, maintained or endorsed by Instagram or any of its affiliates or subsidiaries. Use at your own risk.

# License

Licensed under MIT License.