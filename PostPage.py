
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

        if not post:
            self.write("There is no post with that id number!")
            return
        else:
            self.render("permalink.html", comments = comments, post = post,
                        likes = likes)





    def post(self, post_id):
        post_key = db.Key.from_path("Post", int(post_id),
                                    parent=Post.blog_key())
        post = db.get(post_key)

        creator = post.creator
        user = ''

        comments = get_comments(post_id)

        likes_list = post.likes
        likes = len(likes_list)

        edit_post = False

        error = ''


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
            self.redirect("/")


        if self.request.get("change"):
            post.content = self.request.get("change")
            post.put()
            edit_post = False
            self.redirect("/")


        if self.request.get('edit'):
            if (creator == user):
                edit_post = True
            else:
                error = "Only the author can edit this post!"


        if self.request.get("delete_post"):
            if (creator == user):
                db.delete(post_key)
                self.redirect("/")
            else:
                error = "You can only delete your own posts."


        if self.request.get("likes"):
            if (creator == user):
                error = "You cannot like your own post!"
            else:
                if not (user in likes_list):
                    post.likes.append(user)
                    post.put()
                    likes = len(likes_list)
                else:
                    error = "You have already liked this post!"


        self.render("permalink.html", comments = comments, post = post,
                    likes = likes, error = error, edit_post = edit_post)
