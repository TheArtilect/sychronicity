
from Handler import Handler
from Post import Post
from Comment import Comment

from google.appengine.ext import db
from User import User

class PostPage(Handler):
    def get(self, post_id):
        post_key = db.Key.from_path("Post", int(post_id), parent=Post.blog_key())
        post = db.get(post_key)
        # add comments already submitted
        user = ''
        if self.user:
            user = self.user

        if not post:
            self.write("There is post with that id number!")
            return
        else:
            self.render("permalink.html", post = post, user = user)


    def post(self, post_id):
        post_key = db.Key.from_path("Post", int(post_id),
                                    parent=Post.blog_key())
        post = db.get(post_key)

        if not self.user:
            self.redirect("/login")

        if self.user.name == post.creator:
            comment = self.request.get("comment")
            user = self.user.name
            p_id = post_id
            comment_obj = Comment(parent = Post.comment_key(),
                                    user = user,
                                    p_id = p_id,
                                    comment = comment
                                    )
            comment_obj.put()
            self.render("permalink.html", post = post, user = user)

    #
    # def post(self, post_id):
    #     post_key = db.Key.from_path("Post", int(post_id), parent=Post.blog_key())
    #     post = db.get(post_key)
    #
    #     user = ''
    #     if self.user:
    #         user = self.user
