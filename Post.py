
from google.appengine.ext import db

class Post(db.Model):
    title = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    creator = db.StringProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)
    likes = db.StringListProperty()
    comments = db.StringListProperty()


    def rendered_content(self):
        return self.content.replace("\n", "<br>")

    def render_back(self):
        return self.content.replace("<br>", "\n")

    def number_of_likes(self):
        return len(self.likes)

    def number_of_comments(self):
        return len(self.comments)


def blog_key(name = 'default'):
    return db.Key.from_path('/', name)
