
from Handler import Handler
import Post
import Comment
import time

from google.appengine.ext import db

class DeleteComment(Handler):
    '''
    '''
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

        return self.render("delete_comment.html", comment = comment)


    def post(self, comment_id):
        comment_key = db.Key.from_path("Comment", int(comment_id), parent=Comment.comment_key())
        comment = db.get(comment_key)
        post_id = int(comment.p_id)

        if self.request.get("cancel_delete_comment"):
            return self.redirect("/%s" % post_id)

        if self.request.get('delete_comment'):
            post_key = db.Key.from_path("Post", post_id, parent=Post.blog_key())
            post = db.get(post_key)
            post.comments.remove(str(comment_key))
            post.put()
            db.delete(comment_key)
            time.sleep(0.1)
            return self.redirect("/%s" % post_id)
