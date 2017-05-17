import re


from Handler import Handler
from User import User

class SignUpPage(Handler):
    """
    This class is a child of Handler and is for SignUpPage.
    """
    def get(self):
        return self.render("sign_up.html")

    def post(self):
        self.username = self.request.get("username")
        self.password = self.request.get("password")
        self.verify =  self.request.get("verify")
        self.email = self.request.get("email")

        params = dict(username = self.username,
                        email = self.email)

        if not valid_username(self.username):
            params['error_username'] = "Not a valid username."

        if not valid_password(self.password):
            params["error_password"] = "Not a valid password."
        elif self.password != self.verify:
            params['error_verify'] = "Your passwords don't match."

        if not valid_email(self.email):
            params['error_email'] = "Not a valid email."

        if len(params) > 2:
            return self.render("sign_up.html", **params)
        else:
            self.done()

    def done(self):
        user = User.retrieve_by_name(self.username)
        if user:
            error_message = "User already exists."
            self.render("sign_up.html", error_username = error_message)
        else:
            user = User.register(self.username, self.password, self.email)
            user.put()

            self.login(user)
            return self.render("welcome.html", username = self.username)


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")

PASSWORD_RE = re.compile(r"^.{3,20}$")

EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")

def valid_username(username):
    """
    valid_username: Method for checking if a user name is valid.
    Args:
        username (data type: str):  A user's name.
    Returns:
        True or False
    """
    return username and USER_RE.match(username)


def valid_password(password):
    """
    valid_password: Method for checking if a user password is valid.
    Args:
        password (data type: str):  A user's password.
    Returns:
        True or False
    """
    return password and PASSWORD_RE.match(password)


def valid_email(email):
    """
    valid_email: Method for checking if a user's email is valid.
    Args:
        email (data type: str):  A user's email.
    Returns:
        True or False.
    """
    return not email or EMAIL_RE.match(email)
