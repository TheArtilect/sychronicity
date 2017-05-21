from Handler import Handler
import Post
import Comment
import time

from google.appengine.ext import db

class EditComment(Handler):

    def get(self, comment_id):
        comment_key = db.Key.from_path("Comment", int(comment_id), parent=Comment.comment_key())
        comment = db.get(comment_key)
        post_id = comment.p_id

        post_key = db.Key.from_path("Post", int(post_id), parent=Post.blog_key())
        post = db.get(post_key)

        if not self.user:
            return self.redirect("/login")

        if not (self.user.name == comment.user):
            error = "You can only edit your own comments!"
            return self.redirect("/")

        return self.render("edit_comment.html", comment = comment)


    def post(self, comment_id):
        comment_key = db.Key.from_path("Comment", int(comment_id), parent=Comment.comment_key())
        comment = db.get(comment_key)
        if self.request.get('edit_comment_textarea'):
            comment.comment = self.request.get('edit_comment_textarea')
            comment.put()
            time.sleep(0.1)
            return self.redirect("/%s" % comment.p_id)
