
from Handler import Handler
import Post
import Comment

from google.appengine.ext import db


def get_comments(post_id):
    return db.GqlQuery("SELECT * FROM Comment WHERE p_id='%s' ORDER BY created DESC " % post_id)



class PostPage(Handler):
    def get(self, post_id):
        post_key = db.Key.from_path("Post", int(post_id),
                                    parent=Post.blog_key())
        post = db.get(post_key)
        likes = len(post.likes)

        comments = get_comments(post_id)

        user = ''
        if self.user:
            user = self.user

        if not post:
            self.write("There is no post with that id number!")
            return
        else:
            self.render("permalink.html", comments = comments, post = post, user = user, likes = likes)





    def post(self, post_id):
        post_key = db.Key.from_path("Post", int(post_id),
                                    parent=Post.blog_key())
        post = db.get(post_key)
        creator = post.creator

        likes_list = post.likes
        likes = len(likes_list)




        if not self.user:
            self.redirect("/login")

        user = self.user.name


        if self.request.get("comment"):
            comment = self.request.get("comment")
            p_id = post_id
            comment_obj = Comment.Comment(parent = Comment.comment_key(),
                                    p_id = p_id,
                                    user = user,
                                    comment = comment
                                    )
            comment_obj.put()


        comments = get_comments(post_id)


        if (creator == user) and (self.request.get("delete_post")):
            db.delete(post_key)
            self.redirect("/")

        if (not user in likes_list) and (self.request.get("likes")):
            post.likes.append(user)
            post.put()
            likes = len(likes_list)


        self.render("permalink.html", comments = comments, post = post, user = user, likes = likes)
