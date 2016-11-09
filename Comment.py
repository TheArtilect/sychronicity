from google.appengine.ext import db

def comment_key(name = 'default'):
    return db.Key.from_path('comments', name)



class Comment(db.Model):
    user = db.StringProperty(required = True)
    p_id = db.StringProperty(required = True)
    comment = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)

    @classmethod
    def retrieve_by_p_id(cls, p_id):
        comments = Comment.all().filter("p_id = ", p_id).get()
        return comments

    def rendered_comment(self):
        return self.comment.replace("\n", "<br>")
