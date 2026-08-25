from functools import wraps

from flask import abort, flash, redirect, url_for


def login_required(f):
    """Redirect to login if the user is not authenticated."""
    @wraps(f)
    def decorated(*args, **kwargs):
        from flask_login import current_user
        if not current_user.is_authenticated:
            flash("Faça login para acessar esta página.", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated


def role_required(*roles):
    """Abort 403 if the authenticated user's role is not in the allowed list.

    Accepts UserRole enum values or their string equivalents.
    """
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            from flask_login import current_user
            if not current_user.is_authenticated:
                flash("Faça login para acessar esta página.", "warning")
                return redirect(url_for("auth.login"))
            allowed = {r.value if hasattr(r, "value") else r for r in roles}
            user_role = current_user.role.value if hasattr(current_user.role, "value") else current_user.role
            if user_role not in allowed:
                abort(403)
            return f(*args, **kwargs)
        return decorated
    return decorator
