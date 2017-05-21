
from Handler import Handler
import Post
import Comment

from google.appengine.ext import db


def get_comments(post_id):
    """
    get_comments: Method for getting comments for a blog post.
    Args:
        post_id (str): Blog post key id.

    Returns:
        Array of comments
    """
    return db.GqlQuery("SELECT * FROM Comment WHERE p_id='%s' ORDER BY created DESC" % str(post_id))


class PostPage(Handler):
    """
    This class is a child of Handler and for is PostPage.
    """

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
            return self.render("permalink.html", comments = comments, post = post,
                        likes = likes, user_already_liked = user_already_liked)





    def post(self, post_id):
        post_key = db.Key.from_path("Post", int(post_id),
                                    parent=Post.blog_key())
        post = db.get(post_key)

        creator = post.creator
        user = ''
        error= ''
        comments = get_comments(post_id)

        likes_list = post.likes
        likes = len(likes_list)

        if not self.user:
            return self.redirect("/login")
        else:
            user = self.user.name

        user_already_liked = (user in likes_list)

        if (not self.user) and self.request.get("comment"):
            return self.redirect("/login")


        if self.request.get('edit'):
            if (creator == user):
                return self.redirect("/edit/%s" % post_id)
            else:
                error = "Only the author can edit this post!"


        if self.request.get("delete_post"):
            if (creator == user):
                return self.redirect("/delete/%s" % post_id)
            else:
                error = "You can only delete your own posts."


        if self.request.get("comment"):
            if not user:
                return self.redirect("/login")
            else:
                return self.redirect('/comment/new/%s' % post_id)


        # if self.request.get("comment") and self.user:
        #     comment = self.request.get("comment")
        #     p_id = post_id
        #     comment_obj = Comment.Comment(parent = Comment.comment_key(),
        #                             p_id = p_id,
        #                             user = user,
        #                             comment = comment
        #                             )
        #     comment_key = comment_obj.put()
        #     post.comments.append(str(comment_key))
        #     post.put()
        #
        #
        # if self.request.get("delete_comment"):
        #     comment_id = self.request.get("comment_id")
        #     comment_key = db.Key.from_path("Comment", int(comment_id),
        #                                     parent=Comment.comment_key())
        #     comment = db.get(comment_key)
        #     if (comment) and (user == comment.user):
        #         db.delete(comment_key)
        #         post.comments.remove(str(comment_key))
        #         post.put()
        #
        #     else:
        #         error = "Only the author of this comment can delete it!"
        #
        #
        # if self.request.get("edit_comment"):
        #     comment_id = self.request.get("comment_key_id")
        #     comment_key = db.Key.from_path("Comment", int(comment_id),
        #                                     parent=Comment.comment_key())
        #     comment = db.get(comment_key)
        #     if (comment) and (comment.user == user):
        #         self.render("edit_comment.html", comment = comment, post = post)
        #     else:
        #         error = "You can only edit your own comments."
        #
        #
        #
        # if self.request.get("edit_comment_textarea"):
        #     comment_id = self.request.get("comment_key_id")
        #     comment_key = db.Key.from_path("Comment", int(comment_id),
        #                                     parent=Comment.comment_key())
        #     comment = db.get(comment_key)
        #     if (comment) and (comment.user == user):
        #         comment.comment = self.request.get("edit_comment_textarea")
        #         comment.put()
        #         return self.redirect("%s" % post_id)



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


        return self.render("permalink.html", comments = comments,
                    post = post, likes = likes, error=error,
                    user_already_liked = user_already_liked)
