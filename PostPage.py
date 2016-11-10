import os
import jinja2
import webapp2


from User import User

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

from Handler import Handler
import Post
import Comment

from google.appengine.ext import db


def get_comments(post_id):
    return db.GqlQuery("SELECT * FROM Comment WHERE p_id='%s' ORDER BY created DESC " % post_id)



class PostPage(Handler):
    def get(self, post_id):
        post_key = db.Key.from_path("Post", int(post_id), parent=Post.blog_key())
        post = db.get(post_key)

        comments = get_comments(post_id)

        user = ''
        if self.user:
            user = self.user

        if not post:
            self.write("There is no post with that id number!")
            return
        else:
            self.render("permalink.html", comments = comments, post = post, user = user)





    def post(self, post_id):
        post_key = db.Key.from_path("Post", int(post_id), parent=Post.blog_key())
        post = db.get(post_key)

        if not self.user:
            self.redirect("/login")

        if self.user:
            comment = self.request.get("comment")
            user = self.user.name
            p_id = post_id
            comment_obj = Comment.Comment(parent = Comment.comment_key(),
                                    user = user,
                                    p_id = p_id,
                                    comment = comment
                                    )
            comment_obj.put()

        comments = get_comments(post_id)

        self.render("permalink.html", comments = comments, post = post, user = user)
