from google.appengine.ext import db

def comment_key(name = 'default'):
    return db.Key.from_path('comments', name)


### make comments a Post property

class Comment(db.Model):
    user = db.StringProperty(required = True)
    p_id = db.StringProperty(required = True)
    comment = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)


    #   need to add likes
    def rendered_content(self):
        return self.content.replace("\n", "<br>")
