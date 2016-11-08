import os
import jinja2
import webapp2
import hmac

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)


def make_secure(unsecured):
    return '%s|%s' % (hmac.new(phrase, unsecured).hexdigest(), unsecured)

def check_secure(secured_pass):
    unsecured = secured_pass.split('|')[1]
    if secured_pass == make_secure(unsecured):
        return unsecured


class Handler(webapp2.RequestHandler):
    # def render_str(self, template, **params):
    #     params['user'] = self.user
    #     return render_str(template, **params)

    def write(self, *a, **keywords):
        self.response.out.write(*a, **keywords)

    #   might not work
    def render_str(self, template, **params):
        temp = jinja_env.get_template(template)
        params['user'] = self.user
        return temp.render(params)

    def render(self, template, **keywords):
        self.write(self.render_str(template, **keywords))

    def set_secure_cookie(self, name, value):
        secured_cookie = make_secure(value)
        self.response.headers.add_header(
            'Set-Cookie',
            "%s=%s; Path=/" % (name, secured_cookie)
        )


    def read_secure_cookie(self, name):
        secured_cookie = self.request.cookies.get(name)
        return secured_cookie and check_secure(secured_cookie)

    def login(self, user):
        user_id = str(user.key().id())
        self.set_secure_cookie('user_id', user_id)

    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        user_id = self.read_secure_cookie('user_id')
        self.user = user_id and User.by_id(int(user_id))
