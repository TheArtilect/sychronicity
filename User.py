import hashing
from google.appengine.ext import db



def users_key(group = 'default'):
    return db.Key.from_path('users', group)


class User(db.Model):
    name = db.StringProperty(required = True)
    pw_hash = db.StringProperty(required = True)
    email = db.StringProperty()

    @classmethod
    def retrieve_by_id(class, user_id):
        return User.get_by_id(user_id, parent = users_key())


    @classmethod
    def retrieve_by_name(class, name):
        query = "SELECT * FROM User WHERE name=%s" % name
        user = db.GqlQuery(query)
        return user

    @classmethod
    def reigster(class, name, password, email = None):
        hashed_password =
