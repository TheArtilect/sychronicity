
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
            self.render("permalink.html", comments = comments, post = post,
                        user = user, likes = likes)





    def post(self, post_id):
        post_key = db.Key.from_path("Post", int(post_id),
                                    parent=Post.blog_key())
        post = db.get(post_key)
        creator = post.creator

        likes_list = post.likes
        likes = len(likes_list)



        user = ''
        if not self.user:
            self.redirect("/login")
        else:
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


        error_delete = ''
        if (creator == user) and (self.request.get("delete_post")):
            db.delete(post_key)
            self.redirect("/")
        elif (creator != user) and (self.request.get("delete_post")):
            error_delete = "You can only delete your own posts."


        error_like = ''
        if (not user in likes_list) and (self.request.get("likes") and
            (creator != user)):
            post.likes.append(user)
            post.put()
            likes = len(likes_list)
        else:
            if (user in likes_list) and (self.request.get("likes")):
                error_like = "You have already liked this post!"
            if (creator == user) and (self.request.get("likes")):
                error_like = "You cannot like your own post!"


        self.render("permalink.html", comments = comments, post = post,
                    user = user, likes = likes, error_delete = error_delete,
                    error_like = error_like)
