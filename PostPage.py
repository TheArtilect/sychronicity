
from Handler import Handler
import Post

from google.appengine.ext import db
from User import User

class PostPage(Handler):
    def get(self, post_id):
        post_key = db.Key.from_path("Post", int(post_id), parent=Post.blog_key())
        post = db.get(post_key)

        user = ''
        if self.user:
            user = self.user

        if not post:
            self.write("There is post with that id number!")
            return
        else:
            self.render("permalink.html", post = post, user = user)

    #
    # def post(self, post_id):
    #     post_key = db.Key.from_path("Post", int(post_id), parent=Post.blog_key())
    #     post = db.get(post_key)
    #
    #     user = ''
    #     if self.user:
    #         user = self.user
