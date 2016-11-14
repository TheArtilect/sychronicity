
import random
import hashlib
from string import letters

from google.appengine.ext import db




def make_salt():
    string = ''
    for x in range(0,5):
        string += random.choice(letters)
    return string


def make_pass_hash(name, password, salt = None):
    if not salt:
        salt = make_salt()
    hashed = hashlib.sha256(name + password + salt).hexdigest()
    return '%s|%s' % (hashed, salt)


def valid_pass(name, password, hashed):
    salt = hashed.split('|')[1]
    return hashed == make_pass_hash(name, password, salt)


def users_key(group = 'default'):
    return db.Key.from_path('users', group)


class User(db.Model):
    name = db.StringProperty(required = True)
    pass_hash = db.StringProperty(required = True)
    email = db.StringProperty()

    @classmethod
    def retrieve_by_id(cls, user_id):
        return User.get_by_id(user_id, parent = users_key())


    @classmethod
    def retrieve_by_name(cls, name):
        #   query = "SELECT * FROM User WHERE name=%s" % name
        user = User.all().filter('name =', name).get()
        return user

    @classmethod
    def register (cls, name, password, email = None):
        pass_hash = make_pass_hash(name, password)
        return User( parent = users_key(),
                    name = name,
                    pass_hash = pass_hash,
                    email = email
                    )

    @classmethod
    def login(cls,name, password):
        user = cls.retrieve_by_name(name)
        if user and valid_pass(name, password, user.pass_hash):
            return user
