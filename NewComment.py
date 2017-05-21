from Handler import Handler
import Post
import Comment
import time

from google.appengine.ext import db


class NewComment(Handler):
    '''
    This class is a child of Handler and is for new comments.
    '''

    def get_comments(self, post_id):
        """
        get_comments: Method for getting comments for a blog post.
        Args:
            post_id (str): Blog post key id.

        Returns:
            Array of comments
        """
        return db.GqlQuery("SELECT * FROM Comment WHERE p_id='%s' ORDER BY created DESC" % str(post_id))

    def get(self, post_id):

        if not self.user:
            return redirect("/")

        post_key = db.Key.from_path("Post", int(post_id),
                                    parent=Post.blog_key())
        post = db.get(post_key)

        if not post:
            return self.write("There is no post with that id number!")

        comments = self.get_comments(post_id)

        return self.render("new_comment.html", post=post, comments=comments)


    def post(self, post_id):
        post_key = db.Key.from_path("Post", int(post_id),
                                    parent=Post.blog_key())
        post = db.get(post_key)

        if self.request.get('comment'):

            comment = self.request.get("comment")
            user = self.user.name
            p_id = post_id



            comment_obj = Comment.Comment(parent=Comment.comment_key(),
                                            p_id=p_id,
                                            user=user,
                                            comment=comment
                                            )
            comment_key = comment_obj.put()
            post.comments.append(str(comment_key))
            post.put()
            time.sleep(0.1)
            return self.redirect("/%s" % post_id)
