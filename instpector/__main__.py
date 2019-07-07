from sys import argv
from instpector.instpector import Instpector

def main():
    if len(argv) < 4:
        print((
            "Missing arguments: "
            "--user {user} "
            "--password {password} "
        ))
        return

    instance = Instpector()
    instance.login(user=argv[2], password=argv[4])
    instance.logout()

if __name__ == "__main__":
    main()
