from google.appengine.ext import db

class Comment(db.Model):
    """
    This class is for comments
    Attributes:
        p_id (str): Post key id.
        user (str): Author of the comment.
        comment (str): Content of the comment.
        created (date): Date of when the comment was created.
        last_modified (date): Date of when the comment was last modified.
    """
    p_id = db.StringProperty(required = True)
    user = db.StringProperty(required = True)
    comment = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)


    @classmethod
    def retrieve_by_p_id(cls, p_id):
        """
        retrieve_by_p_id: Method for retrieving comments of a blog post by the
                            post's key id.
        Args:
            p_id (data type: str): String of blog post key id.
        Returns:
            Array of comments belonging to a blog post.
        """
        comments = Comment.all().filter("p_id = ", p_id).get()
        return comments


    def rendered_comment(self):
        """
        rendered_comment:  Method for retaining the multiline format of the
                            blogpost.
        Returns:
            String of comment content with newlines replaced with html breaks.
        """
        return self.comment.replace("\n", "<br>")

    def unrender_comment(self):
        """
        unrender_comment:  Method for retaining the multiline format of the
                            blogpost after being retrieved from the database.
        Returns:
            String of comment content with html breaks replaced with new line
            breaks.
        """
        return self.comment.replace("<br>", "\n")



def comment_key(name = 'default'):
    return db.Key.from_path('comments', name)
