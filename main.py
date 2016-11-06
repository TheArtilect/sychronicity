import os
import jinja2
import webapp2

import hashing
import signup

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)


# def render_str(template, **params):
#     temp = jinja_env.get_template(template)
#     return temp.render(params)

# class Post(db.Model):
#     title = db.StringProperty(required = True)
#     content = db.TextProperty(required = True)
#     created = db.DateTimeProperty(auto_now_add = True)
#     last_modified = db.DateTimeProperty(auto_now = True)
#     #   need to add the user that created it, likes, comments
#
#     def render(self):
#         self._render_text = self.content.replace("\n", "<br>")
#         return render_str("post.html", p = self)



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



class FrontPage(Handler):
    def get(self):
        #posts = db.GqlQuery("SELECT * From Post ORDER BY created DESC LIMIT 10")
        self.render("frontpage.html")


app = webapp2.WSGIApplication([ ("/", FrontPage)
                                ],
                                debug=True)
