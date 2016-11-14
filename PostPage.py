
from Handler import Handler
import Post
import Comment

from google.appengine.ext import db


def get_comments(post_id):
    return db.GqlQuery("SELECT * FROM Comment WHERE p_id='%s' ORDER BY created DESC" % post_id)

class PostPage(Handler):
    def get(self, post_id):
        post_key = db.Key.from_path("Post", int(post_id),
                                    parent=Post.blog_key())
        post = db.get(post_key)
        likes_list = post.likes
        likes = len(post.likes)
        if self.user:
            user = self.user.name
        else:
            user = ""

        user_already_liked = user in likes_list
        comments = get_comments(post_id)



        if not post:
            self.write("There is no post with that id number!")
            return
        else:
            self.render("permalink.html", comments = comments, post = post,
                        likes = likes, user_already_liked = user_already_liked)





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

        user_already_liked = (user in likes_list)

        if (not self.user) and self.request.get("comment"):
            self.redirect("/login")

        if self.request.get("comment") and self.user:
            comment = self.request.get("comment")
            p_id = post_id
            comment_obj = Comment.Comment(parent = Comment.Comment.comment_key(),
                                    p_id = p_id,
                                    user = user,
                                    comment = comment
                                    )
            comment_key = comment_obj.put()
            post.comments.append(str(comment_key))
            post.put()


        if self.request.get("delete_comment"):
            comment_id = self.request.get("comment_id")
            comment_key = db.Key.from_path("Comment", int(comment_id),
                                            parent=Comment.Comment.comment_key())
            comment = db.get(comment_key)
            if user == comment.user:
                db.delete(comment_key)
                post.comments.remove(str(comment_key))
                post.put()

            else:
                error = "Only the author of this comment can delete it!"


        if self.request.get("edit_comment"):
            comment_id = self.request.get("comment_key_id")
            comment_key = db.Key.from_path("Comment", int(comment_id),
                                            parent=Comment.Comment.comment_key())
            comment = db.get(comment_key)
            if comment.user == user:
                self.render("edit_comment.html", comment = comment, post = post)
            else:
                error = "You can only edit your own comments."



        if self.request.get("edit_comment_textarea"):
            comment_id = self.request.get("comment_key_id")
            comment_key = db.Key.from_path("Comment", int(comment_id),
                                            parent=Comment.Comment.comment_key())
            comment = db.get(comment_key)
            comment.comment = self.request.get("edit_comment_textarea")
            comment.put()
            self.redirect("%s" % post_id)


        if (self.request.get("change-title")) or (self.request.get("change-content")):
            post.title = self.request.get("change-title")
            post.content = self.request.get("change-content")
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


        if self.request.get("likes") and user:
            if (creator == user):
                error = "You cannot like your own post!"
            else:
                if not (user in likes_list):
                    post.likes.append(user)
                    post.put()



        if self.request.get("unlike") and user:
            post.likes.remove(user)
            post.put()




        self.render("permalink.html", comments = comments, post = post,
                    likes = likes, error = error, edit_post = edit_post,
                    user_already_liked = user_already_liked)
                    #edit_comment = edit_comment, comment_obj = comment_obj)
