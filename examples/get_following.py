from sys import argv
from context import Instpector #pylint: disable=no-name-in-module

def get_following(**options):
    instpector = Instpector({
        "ig_app_id": options.get("ig_app_id"),
        "ig_ajax_id": options.get("ig_ajax_id")
    })
    if not instpector.login(user=options.get("user"), password=options.get("password")):
        return

    following = instpector.following()

    for followee in following.get_all_for(options.get("target_user_id")):
        print(followee)

    instpector.logout()

if __name__ == '__main__':
    if len(argv) < 10:
        print((
            "Missing arguments: "
            "--user {user} "
            "--password {password} "
            "--target_user_id {user_id}"
            "--app_id {app_id} "
            "--ajax_id {ajax_id}"
        ))
        exit(1)
    get_following(
        user=argv[2],
        password=argv[4],
        target_user_id=argv[6],
        ig_app_id=argv[8],
        ig_ajax_id=argv[10]
    )
