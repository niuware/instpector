from sys import argv
from context import Instpector, endpoints

def get_timeline(**options):
    instpector = Instpector()
    if not instpector.login(user=options.get("user"), password=options.get("password")):
        return

    timeline = endpoints.factory.create("timeline", instpector)
    comments = endpoints.factory.create("comments", instpector)

    for post in timeline.of_user(options.get("target_user_id")):
        print(post)
        for comment in comments.of_post(post):
            print(comment)
            ### Like a comment:
            # comments.like(comment)
            ### Unlike a comment:
            # comments.unlike(comment)
            if comment.thread_count > 0:
                for thread_comment in comments.of_comment(comment):
                    print(thread_comment)

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
