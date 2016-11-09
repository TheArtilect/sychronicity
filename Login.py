from Handler import Handler
from User import User

class Login(Handler):
    def get(self):
        self.render("login.html")

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")

        user = User.login(username, password)
        if user:
            self.login(user)
            self.redirect("/welcome")
        else:
            error_message = "Invalid login"
            self.render("login.html", error = error_message)
