from sys import argv
from context import Instpector, endpoints

def get_story_reel(**options):

    instpector = Instpector()
    if not instpector.login(user=options.get("user"), password=options.get("password")):
        return

    profile = endpoints.factory.create("profile", instpector)
    story_reel = endpoints.factory.create("story_reel", instpector)
    story = endpoints.factory.create("story", instpector)

    target_profile = profile.of_user(options.get("target_username"))

    for story_item in story_reel.of_user(target_profile.id):
        print(story_item.view_count)
        for viewer in story.viewers_for(story_item.id):
            print(viewer.username)

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
    get_story_reel(
        user=argv[2],
        password=argv[4],
        target_username=argv[6]
    )
