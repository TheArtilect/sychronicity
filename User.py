import hashing
from google.appengine.ext import db



def users_key(group = 'default'):
    return db.Key.from_path('users', group)


class User(db.Model):
    name = db.StringProperty(required = True)
    pass_hash = db.StringProperty(required = True)
    email = db.StringProperty()

    @classmethod
    def retrieve_by_id(class, user_id):
        return User.get_by_id(user_id, parent = users_key())


    @classmethod
    def retrieve_by_name(class, name):
        #   query = "SELECT * FROM User WHERE name=%s" % name
        user = User.all().filter('name =', name).get()
        return user

    @classmethod
    def register (class, name, password, email = None):
        pass_hash = make_pass_hash(name, password)
        return User( parent = users_key(),
                    name = name,
                    pass_hash = pass_hash,
                    email = email
                    )

    @classmethod
    def login(cls,name, password):
        user = cls.by_name(name)
        if user and valid_pass(name, password, user.pass_hash):
            return user
