import os
import jinja2
import webapp2
import hmac

from User import User

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)


phrase = "That'sGold,Jerry.GOLD!"
def make_secure(unsecured):
    """
    make_secure: method for creating a secure password keyed-hash using HMAC
                and a pass phrase.
    Args:
        unsecured (data type: str): string input of user's unsecure password
    Returns:
        returns concatenated string of HMAC keyed-hash password and
            unsecured password
    """
    return '%s|%s' % (hmac.new(phrase, unsecured).hexdigest(), unsecured)



def check_secure(secured_pass):
    """
    make_secure: method for creating a secure password keyed-hash using HMAC
                and a pass phrase.
    Args:
        secured_pass (data type: str): string input of user's hashed password
    Returns:
        True if the secured_pass matches the unsecured password substring after
        it has been hashed.
    """
    unsecured = secured_pass.split('|')[1]
    if secured_pass == make_secure(unsecured):
        return unsecured


class Handler(webapp2.RequestHandler):

    '''
    This class is the parent handler class
    '''


    def write(self, *a, **keywords):
        """
        write:  Method for writing an html response.
        Args:
            *a (data type: str):
            **keywords (data type: str):
        Returns:
            Does not return a value
        """
        self.response.out.write(*a, **keywords)


    def render_str(self, template, **params):
        """
        render_str:  Method for writing an html response.
        Args:
            template (data type: str): Name of html template file.
            **params (data type: list): Parameters and their values.
        Returns:
            Returns a template rendered with the specified parameters as well as
            the user params.
        """
        temp = jinja_env.get_template(template)
        params['user'] = self.user
        return temp.render(params)


    def render(self, template, **keywords):
        """
        render: Method for rendering html page
        Args:
            template (data type: str):  Name of html template file.
            **keywords (data type: list): List of keywords and their values.
        Returns:
            Returns a rendered html template.
        """
        self.write(self.render_str(template, **keywords))


    def set_secure_cookie(self, name, value):
        """
        set_secure_cookie:  Method for setting a secure cookie.
        Args:
            name (data type: str): Name of a cookie.
            value (data type: str): Value of a cookie
        """
        secured_cookie = make_secure(value)
        self.response.headers.add_header(
            'Set-Cookie',
            "%s=%s; Path=/" % (name, secured_cookie)
        )


    def read_secure_cookie(self, name):
        """
        read_secure_cookie:     Method for reading a secure cookie.
        Args:
            name (data type: str): Name of a cookie
        Returns:
            True or False
        """
        secured_cookie = self.request.cookies.get(name)
        return secured_cookie and check_secure(secured_cookie)

    def login(self, user):
        """
        login:  Method for logging a user in.
        Args:
            user_id (data type: str):   The user key id.
        """
        user_id = str(user.key().id())
        self.set_secure_cookie('user_id', user_id)

    def logout(self):
        """
        logout: Method for logging a user out.
        """
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    def initialize(self, *a, **kw):
        """
        initialize: Method for initializing a web page with userinfo.
        """
        webapp2.RequestHandler.initialize(self, *a, **kw)
        user_id = self.read_secure_cookie('user_id')
        self.user = user_id and User.retrieve_by_id(int(user_id))
