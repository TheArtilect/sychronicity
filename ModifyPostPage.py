
from Handler import Handler
import Post


from google.appengine.ext import db

class ModifyPostPage(Handler):
    def get(self):
        post_id = self.request.get("post_id")
        post_key = db.Key.from_path("Post", int(post_id),
                                    parent=Post.blog_key())
        post = db.get(post_key)

        if not post:
            self.write("There is no post with that id number!")
            return

        if self.user != post.creator:
            self.redirect("/")  #make error page
        else:
            self.render("modify_post.html", post = post)
