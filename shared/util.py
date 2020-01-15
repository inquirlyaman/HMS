import re
import configparser
from passlib.hash import pbkdf2_sha256
import os.path
from functools import wraps
from flask import request
import jwt
key = 'HMS'
path = os.path.abspath(os.path.dirname(__file__))
CONFIG_PATH = os.path.join(path, './messageConfig.ini')
ConfigINI = configparser.ConfigParser()
ConfigINI.read(CONFIG_PATH)
VALID_EMAIL_REGEX = re.compile(
            r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
                r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-011\013\014\016-\177])*"' # quoted-string
                    r')@(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?$', re.IGNORECASE)
VALID_MOBILE_REGEX = re.compile("^[0-9]{10}$")
#validate email id 

def validate_email(email_id):
    INVALID_EMAIL = ConfigINI.get('MessageConfig', 'INVALID_EMAIL_MESSAGE')
    if not VALID_EMAIL_REGEX.match(email_id):
        return {'status': 'error','message':INVALID_EMAIL}
    return {'status': 'success'}

#validate mobile
def validate_mobile(mobile_number):
    if not VALID_MOBILE_REGEX.match(mobile_number):
        return {'status': 'error',
                'message': '"'+mobile_number+'" is not a valid mobile number'}
    return {'status': 'success'}

#validate password
def valid_password(passowrd,confirm_password):
    CONFIRM_PASSWORD = ConfigINI.get('MessageConfig', 'CONFIRM_PASSWORD_MESSAGE')
    if( passowrd != confirm_password):
        return {'status': 'error','message':CONFIRM_PASSWORD}
    return {'status': 'success'}

#password hash
def password_hash(password):
    hash_password = pbkdf2_sha256.hash(password)
    return hash_password
#verify password  hash
def verify_password(password,hash_password):
    return pbkdf2_sha256.verify(password,hash_password)

# Here is a custom decorator that verifies the JWT is present in
# the request, as well as insuring that this user has a role of
# `admin` in the access token
def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        access_token = request.headers.get('token')
        if not access_token:
            return dict(status='error',
                    message ='Token is missing '),403
        try:
            data = jwt.decode(access_token, key)
            print(data)
        except:
            return dict(status='error',
                    message ='Token is invalid '),403
        
        return f(*args,**kwargs)
    return decorated
def is_admin(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        access_token = request.headers.get('token')
        if not access_token:
            return dict(status='error',
                    message ='Token is missing '),403
        try:
            data = jwt.decode(access_token, key)
            if(data['user']['role'] != 'admin') :
                return dict(status='error', message='Access Forbidden'),403
        except:
            return dict(status='error',
                    message ='Token is invalid '),403
        return f(*args,**kwargs)
    return decorated
