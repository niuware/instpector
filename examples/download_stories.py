from sys import argv
from context import Instpector, endpoints

def download_stories(**options):

    instpector = Instpector()
    if not instpector.login(user=options.get("user"), password=options.get("password")):
        return

    profile = endpoints.factory.create("profile", instpector)
    story_reel = endpoints.factory.create("story_reel", instpector)

    target_profile = profile.of_user(options.get("target_username"))

    for story_item in story_reel.of_user(target_profile.id):
        story_reel.download(story_item)

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
    download_stories(
        user=argv[2],
        password=argv[4],
        target_username=argv[6]
    )
