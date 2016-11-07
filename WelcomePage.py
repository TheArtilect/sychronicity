from Handler import Handler

class WelcomePage(Handler):
    def get(self):
        self.render("welcome.html", username = username)
