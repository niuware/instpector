# Instpector

The Instagram web command line interface tool.

# Installation

```
pip install instpector
```

# Example

```python
from instpector import Instpector

instpector = Instpector()

# Login to Instagram web
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

# Current APIs

- Followers   
- Following   
- Timeline   
- Profile   

# Disclaimer

This tool is not affiliated with, authorized, maintained or endorsed by Instagram or any of its affiliates or subsidiaries. Use at your own risk.

# License

Licensed under MIT License.