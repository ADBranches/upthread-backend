from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.utils.auth_utils import role_required
from app.models import User, UserSchema

protected_bp = Blueprint("protected", __name__, url_prefix="/api/v1")

user_schema = UserSchema()
users_schema = UserSchema(many=True)


@protected_bp.get("/me")
@jwt_required()
def me():
    user_id = get_jwt_identity()   # now returns a string ID
    claims = get_jwt()
    role = claims.get("role")

    user = User.query.get(int(user_id))
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "role": role
    }), 200


@protected_bp.get("/admin/users")
@role_required("admin")
def list_users():
    users = User.query.all()
    return users_schema.jsonify(users), 200
