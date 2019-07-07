from sys import argv
from context import Instpector, endpoints

def get_timeline(**options):
    instpector = Instpector()
    if not instpector.login(user=options.get("user"), password=options.get("password")):
        return

    timeline = endpoints.factory.create("timeline", instpector)

    for post in timeline.get_all_for(options.get("target_user_id")):
        print(post)

    instpector.logout()

if __name__ == '__main__':
    if len(argv) < 6:
        print((
            "Missing arguments: "
            "--user {user} "
            "--password {password} "
            "--target_user_id {user_id}"
        ))
        exit(1)
    get_timeline(
        user=argv[2],
        password=argv[4],
        target_user_id=argv[6]
    )
