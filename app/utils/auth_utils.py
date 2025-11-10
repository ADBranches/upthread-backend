# app/utils/auth_utils.py
from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def role_required(*roles):
    """
    Example:
    @role_required("admin")
    @role_required("admin", "manager")
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()           # ✅ new: read JWT claims directly
            role = claims.get("role")    # role stored in additional_claims
            if role not in roles:
                return jsonify({"error": "Forbidden", "detail": "Insufficient role"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator
