import string
from secrets import choice

from redis import StrictRedis

from lock_app.constants import (
    TOKEN_LIFETIME, TOKEN_NUM_PARTS, TOKEN_PART_LENGTH
)
from lock_app.password import check_key


redis_client = StrictRedis()


def authenticate_token(token):
    """
    Given a token, check whether it's valid or not. We can accomplish
    this simply by checking whether it exists in the Redis data store,
    as we're leaving the key expiration up to Redis.
    :param token: The token to authenticate.
    :return: A truthy or falsy value indicating whether the token is valid.
    """
    return redis_client.get(token)


def generate_token_string():
    """
    Helper utility to generate a token string. This is used instead
    of secrets.token_urlsafe as I wanted a guaranteed length for the
    token, rather than a guaranteed number of bytes. I also wanted
    the flexibility to format the token into smaller groups.
    :return: A newly generated, formatted & grouped token.
    """
    alphabet = string.ascii_letters + string.digits
    token_parts = [
        ''.join(choice(alphabet) for _ in range(TOKEN_PART_LENGTH))
        for _ in range(TOKEN_NUM_PARTS)
    ]
    token = '-'.join(token_parts)
    return token


def generate_token(key):
    """
    Check that a key is valid, and if so, generate and return a new token.
    We should also store that token in the local data store, and set its
    expiry time according to the value set in constants.py.
    :param key: The key on whose authority we're generating a new token.
    :return: The generated token, or None if the key wasn't valid.
    """
    if not check_key(key):
        return None

    token = generate_token_string()
    redis_client.set(token, "valid", TOKEN_LIFETIME)
    return token
