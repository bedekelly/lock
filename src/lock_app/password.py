import bcrypt

from lock_app import redis_client
from .constants import SALT
from .keys import MASTER_KEY


def check_key(key):
    """
    Given a key, check whether hashing it matches the hash we've
    stored for the original key. If it does, we know the key matches
    the original key. If not, it doesn't, and we can return False.
    :param key: The key to check against the original key.
    :return: Whether the given key matches the original key or not.
    """

    with open("key.txt", 'rb') as f:
        original = f.read()
    return get_hash(str(key).replace(" ", "")) == original


def save_hash(password_hash):
    """
    Store a binary password hash in a local file.
    :param password_hash: The password hash to save.
    """
    with open("key.txt", 'wb') as f:
        f.write(password_hash)


def get_hash(key):
    """
    Given a "raw" key, salt+hash it to obtain a password hash.
    This hash should not be reversible, so it should be safe to store.
    :param key: The raw key: equivalent to a plaintext password.
    :return: The result of hashing the given key.
    """
    key = str(key).replace(" ", "")
    key = key.encode("utf-8")
    salt = SALT.encode("utf-8")
    master_key = MASTER_KEY.encode("utf-8")
    combo_password = key + salt + master_key
    hashed_password = bcrypt.hashpw(combo_password, salt)
    return hashed_password


def save_key(key):
    """
    Helper utility to generate the hash for a key and write it to a file.
    :param key: The key to hash and write.
    """
    save_key_length(len(key))
    strkey = str(key)
    save_hash(get_hash(strkey))


def save_key_length(n):
    redis_client.set("key_length", n)


def lookup_key_length():
    return redis_client.get("key_length").decode("utf-8")
