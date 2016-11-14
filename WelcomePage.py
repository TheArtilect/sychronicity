from Handler import Handler
import Post
from google.appengine.ext import db

class WelcomePage(Handler):
    def get(self):
        if self.user:
            username = self.user.name
        else:
            self.redirect("/login")

        posts = db.GqlQuery("SELECT * FROM Post WHERE creator='%s' ORDER BY created DESC" % username)

        self.render("welcome.html", username = username, posts = posts)
