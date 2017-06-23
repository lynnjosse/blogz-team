import hashlib
import random
import string

def make_salt():
    return ''.join([random.choice(string.ascii_letters) for x in range(4)])
   
 
def make_pw_hash(password, salt = None):
    if not salt:
        salt = make_salt()
    string_to_hash = password + salt
    return hashlib.sha256(string_to_hash.encode()).hexdigest() + ',' + salt

def check_pw_hash(password, hash):
    salt = hash.split(',')[1]
    if make_pw_hash(password, salt) == hash:
        return True
    return False