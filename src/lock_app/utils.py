from password import check_password
from token import get_token
from constants import BAD_KEY_ERROR


def fetch_token(key):
    if check_password(key):
        return get_token()
    else:
        return BAD_KEY_ERROR
    
