from flask import abort  # type: ignore
from flask_login import current_user  # type: ignore
from functools import wraps


def role_required(roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated or not any(current_user.has_role(role) for role in roles):
                abort(403)
            return func(*args, **kwargs)

        return wrapper

    return decorator
