from Handler import Handler
import Post

class NewPost(Handler):
    """
    This class is a child of Handler and for NewPost.
    """
    def get(self):
        if self.user:
            return self.render("new_post.html")
        else:
            return self.redirect("/login")

    def post(self):
        if not self.user:
            return self.redirect("/login")

        title = self.request.get("title")
        content = self.request.get("content")
        youtube = None
        if self.request.get("youtube"):
            link = self.request.get("youtube")
            try:
                vid_id = link.split("=")[1]
                youtube = vid_id
            except IndexError:
                error = "Requires a valid Youtube Link!"
                return self.render("new_post.html", title=title, content=content, error=error)


        if title and content:
            creator = self.user.name
            posting = Post.Post(parent = Post.blog_key(), title = title,
                                content = content, youtube = youtube, creator = creator)
            posting.put()
            posting_id = posting.key().id()
            return self.redirect("/%s" % str(posting_id))
        else:
            error = "Each post requires both a title and content!"
            return self.render("new_post.html", title=title, content=content, error=error)
