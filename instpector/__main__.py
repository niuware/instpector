from sys import argv
from instpector.instpector import Instpector

def main():
    if len(argv) < 8:
        print((
            "Missing arguments: "
            "--user {user} "
            "--password {password} "
            "--app_id {app_id} "
            "--ajax_id {ajax_id}"
        ))
        return

    instance = Instpector({
        "ig_app_id": argv[6],
        "ig_ajax_id": argv[8]
    })
    instance.login(user=argv[2], password=argv[4])
    instance.logout()

if __name__ == "__main__":
    main()
