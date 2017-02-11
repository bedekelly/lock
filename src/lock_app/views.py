from functools import wraps

from flask import request, jsonify

from lock_app.password import save_key, lookup_key_length
from .constants import KEY_LENGTH, BAD_TOKEN_ERROR, NO_KEY_ERROR, BAD_KEY_ERROR
from .tokenutils import generate_token, authenticate_token


def error(error_text):
    """
    Helper function to format an error message as a JSON response.
    :param error_text: The raw text of the error message to send.
    :return: A JSON response suitable to be returned by a Flask View.
    """
    return jsonify(error=error_text), 400


def message(message_text):
    """
    Helper function to format a message as a JSON response.
    :param message_text: The raw text of the message to send.
    :return: A JSON response suitable to be returned by a Flask View.
    """
    return jsonify(message=message_text)


def get_key_length():
    """
    Flask endpoint which returns the key length as a JSON response.
    """
    return jsonify(keylength=lookup_key_length())


def get_token():
    """
    Flask endpoint which exchanges a valid key for an access token.
    If the key is invalid, an error message will be returned instead.
    If it is valid, the response will be a JSON object with a single
    "token" key containing the generated token.
    """
    key = request.args.get('key')
    if key is None:
        return error(NO_KEY_ERROR)

    token = generate_token(key)
    if token is None:
        return error(BAD_KEY_ERROR)

    return jsonify(token=token)


def token_required(fn):
    """
    Decorator for Flask endpoints to require that requests routed to
    them have a valid "token" parameter. N.B. that this is using the
    "request args" (i.e. ?token=blah) so that the decorator can be
    used for endpoints accepting GET requests, as the GET method does
    not allow a body payload to be sent.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        token = request.args.get("token")
        if authenticate_token(token):
            return fn(*args, **kwargs)
        return error(BAD_TOKEN_ERROR)

    return wrapper


@token_required
def change_key():
    """
    Flask endpoint to change the current key. This endpoint requires
    a valid token to change the key.
    """
    # Todo: Check whether the key is the right length?
    new_key = request.json.get("key")
    if new_key is None:
        return error(BAD_KEY_ERROR)
    save_key(new_key)
    return message("Success!")


@token_required
def get_secret_info():
    """
    Flask endpoint demonstrating that a resource accessible only by
    GET requests can be protected using the @token_required decorator.
    """
    return message("Top-secret information!")


def init(app):
    """
    This function exists to avoid Flask's strange circular-dependency
    behaviour. Instead of importing "app" from the current package
    in order to use the @app.route decorator, here we just write an
    `init` function which takes the `app` object as a parameter and
    registers all the routes manually.
    """
    app.route("/auth/token")(get_token)
    app.route("/auth/keylength")(get_key_length)
    app.route("/auth/key", methods=["POST"])(change_key)
    app.route("/info")(get_secret_info)
