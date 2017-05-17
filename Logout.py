from Handler import Handler

class Logout(Handler):
    """
    This class is a child of Handler and for Logout.
    """
    def get(self):
        self.logout()
        return self.redirect("/signup")
