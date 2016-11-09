
from Handler import Handler
import Post
import Comment

from google.appengine.ext import db


def get_comments(post_id):
    # query_string = "SELECT * FROM Comment WHERE p_id=%s ORDER BY created DESC LIMIT 10" % post_id
    # comments = db.GqlQuery(query_string)
    # return comments
    comments = Comment.Comment.all().filter('p_id =', post_id).get()
    return comments

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
        post_key = db.Key.from_path("Post", int(post_id),
                                    parent=Post.blog_key())
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

        query_string = "SELECT * FROM Comment WHERE p_id='%s' ORDER BY created DESC LIMIT 10" % str(post_id)
        comments = db.GqlQuery(query_string)

        self.render("permalink.html", post = post, user = user, comments = comments)

    #
    # def post(self, post_id):
    #     post_key = db.Key.from_path("Post", int(post_id), parent=Post.blog_key())
    #     post = db.get(post_key)
    #
    #     user = ''
    #     if self.user:
    #         user = self.user
