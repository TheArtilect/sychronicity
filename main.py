
import webapp2

from Handler import Handler
from NewPostPage import NewPost
from PostPage import PostPage
from SignUpPage import SignUpPage
from WelcomePage import WelcomePage
from Login import Login
from Logout import Logout

import Post
import User
import Comment

from google.appengine.ext import db


class FrontPage(Handler):
    """
    This class is a child of Handler and is for FrontPage.
    """
    def get(self):
        user = ''
        if self.user:
            user = self.user.name
        posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC LIMIT 10")
        self.render("frontpage.html", posts = posts, user = user)



app = webapp2.WSGIApplication([ ("/", FrontPage),
                                ("/newpost", NewPost),
                                ('/([0-9]+)', PostPage),
 #                               ('/([0-9]+/delete)', DeletePost),
                                ("/signup", SignUpPage),
                                ("/welcome", WelcomePage),
                                ("/login", Login),
                                ("/logout", Logout)
                                ],
                                debug=True)
