import re
from Handler import Handler


from string import letters




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


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")

PASSWORD_RE = re.compile(r"^.{3,20}$")

EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")

def valid_username(username):
    return username and USER_RE.match(username)

def valid_password(password):
    return password and PASSWORD_RE.match(password)

def valid_email(email):
    return not email or EMAIL_RE.match(email)
