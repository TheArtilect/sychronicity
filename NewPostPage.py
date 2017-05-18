import re
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
                checkQ = link.split("/")[3]
                if '//youtu.be' in link:
                    checkQ = checkQ.replace("?", "&")
                    vid_id, times = checkQ.split("&")
                    times = map(int, re.findall(r'\d+', times))
                    starting = 60 * times[0] + times[1]
                    checkQ = "%s?start=%s" % (vid_id, starting)
                else:
                    checkQ = link.split('=')[1]
                youtube = checkQ
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
