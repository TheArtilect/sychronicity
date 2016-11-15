from google.appengine.ext import db

class Comment(db.Model):
    """
    This class is comments
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
        comments = Comment.all().filter("p_id = ", p_id).get()
        return comments


    def rendered_comment(self):
        return self.comment.replace("\n", "<br>")

    def unrender_comment(self):
        return self.comment.replace("<br>", "\n")



def comment_key(name = 'default'):
    return db.Key.from_path('comments', name)
