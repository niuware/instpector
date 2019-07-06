from sys import argv
from context import Instpector #pylint: disable=no-name-in-module

def get_profile(**options):

    instpector = Instpector()
    if not instpector.login(user=options.get("user"), password=options.get("password")):
        return

    profile = instpector.profile()

    print(profile.get_for(options.get("target_username")))

    instpector.logout()

if __name__ == '__main__':
    if len(argv) < 6:
        print((
            "Missing arguments: "
            "--user {user} "
            "--password {password} "
            "--target_username {username}"
        ))
        exit(1)
    get_profile(
        user=argv[2],
        password=argv[4],
        target_username=argv[6]
    )
