
import webapp2

from Handler import Handler
from NewPostPage import NewPost
from PostPage import PostPage
from EditPost import EditPost
from DeletePost import DeletePost
from NewComment import NewComment
from EditComment import EditComment
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
        return self.render("frontpage.html", posts = posts, user = user)



app = webapp2.WSGIApplication([ ("/", FrontPage),
                                ("/newpost", NewPost),
                                ('/([0-9]+)', PostPage),
                                ('/edit/([0-9]+)', EditPost),
                                ('/delete/([0-9]+)', DeletePost),
                                ('/comment/new/([0-9]+)', NewComment),
                                ('/comment/edit/([0-9]+)', EditComment),
                                ("/signup", SignUpPage),
                                ("/welcome", WelcomePage),
                                ("/login", Login),
                                ("/logout", Logout)
                                ],
                                debug=True)
