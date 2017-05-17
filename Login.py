from Handler import Handler
from User import User

class Login(Handler):
    """
    This class is a child of Handler and is for Login.
    """
    def get(self):
        return self.render("login.html")

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")

        user = User.login(username, password)
        if user:
            self.login(user)
            return self.redirect("/welcome")
        else:
            error_message = "Invalid login"
            return self.render("login.html", error = error_message)
