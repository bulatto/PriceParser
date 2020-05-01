from django.contrib.auth import authenticate


def auth(login, pasword):
    user = authenticate(username=login, password=pasword)
    if user is not None:
        if user.is_active:
            return True, "User is valid, active and authenticated"
        else:
            return True, "The password is valid, but the account has been disabled!"
    else:
        return False, "The username and password were incorrect."
