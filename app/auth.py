import base64
from functools import wraps
from flask import request, abort
from .db_models import User
from werkzeug.security import check_password_hash

def basic_auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Basic '):
            abort(401)  # Unauthorized if header is missing or not Basic Auth

        # Decode the Base64 encoded credentials
        try:
            encoded_credentials = auth_header.split(' ')[1]
            decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
            email, password = decoded_credentials.split(':', 1)
        except Exception:
            abort(401)

        # Look up the user in the database
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            abort(401)  # Unauthorized if credentials are invalid

        # Verify that the user has admin privileges
        if not user.admin:
            abort(403)  # Forbidden if not an admin

        # Optionally, you might want to set a global or context variable here.
        return f(*args, **kwargs)
    return decorated
