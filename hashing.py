import random
import hashlib
import hmac
from string import letters

phrase = "That'sGold,Jerry.GOLD!"


def make_secure_val(val):
    return '%s|%s' % (val, hmac.new(secret, val).hexdigest())

def check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val


def make_salt():
    string = ''
    for x in range(0,5):
        string += random.choice(letters)
    return string


def make_passwordw_hash(name, pw, salt = None):
    if not salt:
        salt = make_salt()
    hashed = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)


def valid_pw(name, password, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(name, password, salt)
