from Handler import Handler
import Post
import Comment
import time

from google.appengine.ext import db

class DeletePost(Handler):
    '''
	This class if a child of PostPage handler and is for editing blog posts.
	'''


    def get(self, post_id):
        post_key = db.Key.from_path("Post", int(post_id), parent=Post.blog_key())
        post = db.get(post_key)

        if not self.user:
            return self.redirect("/login")

        if self.user.name != post.creator:
            return self.redirect('/')

        else:
            return self.render("deletepost.html", post=post)



    def post(self, post_id):
        post_key = db.Key.from_path("Post", int(post_id), parent=Post.blog_key())
        post = db.get(post_key)

        if self.request.get("cancel_delete"):
            return self.redirect("/%s" % post_id)

        if self.request.get('delete_post'):
            db.delete(post_key)
            time.sleep(0.1)
            return self.redirect("/")
