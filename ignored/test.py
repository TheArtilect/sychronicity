import random
import hmac
import hashlib
from string import letters


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

a = make_pass_hash("test", 'test')
print a
print valid_pass('test', 'test', a)
