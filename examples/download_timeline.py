from sys import argv
from context import Instpector, endpoints

def download_timeline(**options):
    instpector = Instpector()
    if not instpector.login(user=options.get("user"), password=options.get("password")):
        return

    profile = endpoints.factory.create("profile", instpector)
    timeline = endpoints.factory.create("timeline", instpector)

    target_profile = profile.of_user(options.get("target_username"))

    for post in timeline.of_user(target_profile.id):
        timeline.download(post)

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
    download_timeline(
        user=argv[2],
        password=argv[4],
        target_username=argv[6]
    )
