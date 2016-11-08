import re
import random
import hmac
from string import letters

from Handler import Handler
from User import User

class SignUpPage(Handler):
    def get(self):
        self.render("sign_up.html")

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        verify =  self.request.get("verify")
        email = self.request.get("email")

        params = dict(username = username,
                        email = email)

        if not valid_username(username):
            params['error_username'] = "Not a valid username."

        if not valid_password(password):
            params["error_password"] = "Not a valid password."
        elif password != verify:
            params['error_verify'] = "Your passwords don't match."

        if not valid_email(email):
            params['error_email'] = "Not a valid email."

        if len(params) > 2:
            self.render("sign_up.html", **params)
        else:
            self.render("welcome.html", username = username)

    def done(self):
        user = User.by_name(self.username)
        if user:
            error_message = "User already exists."
            self.render("sign_up.html", error_username = message)
        else:
            user = User.register(self.username, self.password, self.email)
            user.put()

            self.login(user)
            self.render("welcome.html", username = username)


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")

PASSWORD_RE = re.compile(r"^.{3,20}$")

EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")

def valid_username(username):
    return username and USER_RE.match(username)

def valid_password(password):
    return password and PASSWORD_RE.match(password)

def valid_email(email):
    return not email or EMAIL_RE.match(email)



phrase = "That'sGold,Jerry.GOLD!"

def make_salt():
    string = ''
    for x in range(0,5):
        string += random.choice(letters)
    return string


def make_pass_hash(name, password, salt = None):
    if not salt:
        salt = make_salt()
    hashed = hashlib.sha256(name + password + salt).hexdigest()
    return '%s|%s' % (hashed, salt)


def valid_pass(name, password, hashed):
    salt = hashed.split('|')[1]
    return hashed == make_pass_hash(name, password, salt)
