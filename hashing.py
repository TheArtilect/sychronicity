import random
import hashlib
import hmac
from string import letters

from passphrase import phrase

def make_salt():
    string = ''
    for x in range(0,5):


def make_passwordw_hash(name, pw, salt = None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)

def valid_pw(name, password, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(name, password, salt)
