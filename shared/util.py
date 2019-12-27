import re
import configparser
from passlib.hash import pbkdf2_sha256
import os.path
path = os.path.abspath(os.path.dirname(__file__))
CONFIG_PATH = os.path.join(path, './messageConfig.ini')
ConfigINI = configparser.ConfigParser()
ConfigINI.read(CONFIG_PATH)
VALID_EMAIL_REGEX = re.compile(
            r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
                r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-011\013\014\016-\177])*"' # quoted-string
                    r')@(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?$', re.IGNORECASE)
#validate email id 
def validate_email(email_id):
    INVALID_EMAIL = ConfigINI.get('MessageConfig', 'INVALID_EMAIL_MESSAGE')
    if not VALID_EMAIL_REGEX.match(email_id):
        return {'status': 'error','message':INVALID_EMAIL}
    return {'status': 'success'}
#validate password
def valid_password(passowrd,confirm_password):
    CONFIRM_PASSWORD = ConfigINI.get('MessageConfig', 'CONFIRM_PASSWORD_MESSAGE')
    if( passowrd != confirm_password):
        return {'status': 'error','message':CONFIRM_PASSWORD}
    return {'status': 'success'}
def password_hash(password):
    hash_password = pbkdf2_sha256.hash("password")
    return hash_password