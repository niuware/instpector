# Instpector

The Instagram web command line interface tool.

# Example

```python
instpector = Instpector(configuration)

# Login to Instagram
if not instpector.login("my_username", "password"):
    return

profile = instpector.profile()
followers = instpector.followers()

# Get the profile of any other user
insta_profile = profile.get_for("some_username")

# Iterate over all followers
for follower in followers.get_all_for(insta_profile.id):
    print(follower)
```

# Disclaimer

This tool is not affiliated with, authorized, maintained or endorsed by Instagram or any of its affiliates or subsidiaries. Use at your own risk.

# License

Licensed under MIT License.