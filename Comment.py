from google.appengine.ext import db



class Comment(db.Model):
    p_id = db.StringProperty(required = True)
    user = db.StringProperty(required = True)
    comment = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)

    #   for all comments in a post
    @classmethod
    def retrieve_by_p_id(cls, p_id):
        comments = Comment.all().filter("p_id = ", p_id).get()
        return comments


    def rendered_comment(self):
        return self.comment.replace("\n", "<br>")

    def unrender_comment(self):
        return self.comment.replace("<br>", "\n")



def comment_key(group = 'default'):
    return db.Key.from_path('comments', group)
