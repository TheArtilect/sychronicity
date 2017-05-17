from Handler import Handler
import Post
from google.appengine.ext import db

class WelcomePage(Handler):
    """
    This class is a child of Handler and is for WelcomePage.
    """
    def get(self):
        if self.user:
            username = self.user.name
        else:
            return self.redirect("/login")

        posts = db.GqlQuery("SELECT * FROM Post WHERE creator='%s' ORDER BY created DESC" % username)

        return self.render("welcome.html", username = username, posts = posts)
