# Instpector

A simple Instagram's web API library written in Python. No selenium or webdriver required.

# Installation

```
pip install instpector
```

# Sample usage

```python
from instpector import Instpector, endpoints

instpector = Instpector()

# Login into Instagram's web
instpector.login("my_username", "my_password")

# Get the profile of any user, for example 'some_username'
profile = endpoints.factory.create("profile", instpector)
insta_profile = profile.of_user("some_username")
print(insta_profile)
# id, followers_count, following_count, is_private, ... 

# Iterate all followers of 'some_username'
followers = endpoints.factory.create("followers", instpector)
for follower in followers.of_user(insta_profile.id):
    print(follower)
    # id, username, full_name, ...

# Logout
instpector.logout()
```

Check more in the `examples` directory.

# Available endpoints

- Followers   
- Following   
- Timeline   
- Profile   
- Story Reel    
- Story    

More to come

# Development dependencies

- requests

# Disclaimer

This tool is not affiliated with, authorized, maintained or endorsed by Instagram or any of its affiliates or subsidiaries. Use at your own risk.

# License

Licensed under MIT License.