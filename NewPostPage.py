from Handler import Handler
import Post

class NewPost(Handler):
#   NEED TO ADD TO SEE IF USER IS LOGGED IN
    def get(self):
        self.render("new_post.html")

    def post(self):
#   NEED TO ADD TO SEE IF USER IS LOGGED IN
        title = self.request.get("title")
        content = self.request.get("content")

        if title and content:
            #   add user to this
            posting = Post.Post(parent = Post.blog_key(), title = title,
                                content = content)
            posting.put()
            posting_id = posting.key().id()
            self.redirect("/%s" % str(posting_id))
        else:
            error = "Each post requires both a title and content!"
            self.render("new_post.html", title=title, content=content, error=error)
