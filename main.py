import os
import jinja2
import webapp2

import hashing
import signup

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)


class Handler(webapp2.RequestHandler):
    # def render_str(self, template, **params):
    #     params['user'] = self.user
    #     return render_str(template, **params)

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        temp = jinja_env.get_template(template)
        return temp.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


def blog_key(name = 'default'):
    return db.Key.from_path('/', name)


class Post(db.Model):
    title = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)
    #   need to add the user that created it, likes, comments

    def rendered_content(self):
        return self.content.replace("\n", "<br>")


def render_post(response, post):
    response.out.write('<b>' + post.title + '</b><br>')
    response.out.write(post.content)


class FrontPage(Handler):
    def get(self):
        posts = db.GqlQuery("SELECT * From Post ORDER BY created DESC LIMIT 10")
        self.render("frontpage.html", posts = posts)



class NewPost(Handler):
#   NEED TO ADD TO SEE IF USER IS LOGGED IN
    def get(self):
        self.render("new_post.html")

    def post(self):
#   NEED TO ADD TO SEE IF USER IS LOGGED IN
        title = self.request.get("title")
        content = self.request.get("content")

        if title and content:
            #   add user to this
            posting = Post(parent = blog_key(), title = title, content = content)
            posting.put()
            posting_id = posting.key().id()
            self.redirect("/%s" % str(posting_id))
        else:
            error = "Each post requires both a title and content!"
            self.render("new_post.html", title=title, content=content, error=error)




class PostPage(Handler):
    def get(self, post_id):
        post_key = db.Key.from_path("Post", int(post_id), parent=blog_key())
        post = db.get(post_key)

        if not post:
            self.write("There is post with that id number!")
            return
        else:
            self.render("permalink.html", post = post)




app = webapp2.WSGIApplication([ ("/", FrontPage),
                                ("/newpost", NewPost),
                                ('/([0-9]+)', PostPage)
                                ],
                                debug=True)
