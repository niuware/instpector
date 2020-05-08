from sys import argv
from pyotp import TOTP
from context import Instpector, endpoints

def get_profile(**options):

    instpector = Instpector()
    # Using pyotp for getting the two-factor authentication code
    totp = TOTP(options.get("two_factor_key"))
    if not instpector.login(user=options.get("user"),
                            password=options.get("password"),
                            two_factor_code=totp.now()):
        return

    profile = endpoints.factory.create("profile", instpector)

    print(profile.of_user("target_user_name"))

    instpector.logout()

if __name__ == '__main__':
    if len(argv) < 6:
        print((
            "Missing arguments: "
            "--user {user} "
            "--password {password} "
            "--two_factor_key {two_factor_key}"
        ))
        exit(1)
    get_profile(
        user=argv[2],
        password=argv[4],
        two_factor_key=argv[6]
    )
