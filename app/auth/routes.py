from flask import Blueprint, request, jsonify
from app.models import User, db
from app.extensions import bcrypt
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)

auth_bp = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


# -----------------------------
# REGISTER
# -----------------------------
@auth_bp.post("/register")
def register():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "user")
    full_name = data.get("full_name")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "User already exists"}), 409

    user = User(email=email, role=role, full_name=full_name)
    user.password = password

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


# -----------------------------
# LOGIN
# -----------------------------
@auth_bp.post("/login")
def login():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.verify_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    # ✅ FIX: identity must be a string (JWT spec)
    # Add role as part of "additional_claims"
    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role}
    )
    refresh_token = create_refresh_token(
        identity=str(user.id),
        additional_claims={"role": user.role}
    )

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "full_name": user.full_name,
        }
    }), 200


# -----------------------------
# REFRESH TOKEN
# -----------------------------
@auth_bp.post("/refresh")
@jwt_required(refresh=True)
def refresh():
    current_identity = get_jwt_identity()  # will be user.id (string)
    claims = get_jwt()                     # optional, has "role"
    new_access = create_access_token(
        identity=str(current_identity),  # must be a string, not int, since JWT spec current_identity,
        additional_claims={"role": claims.get("role")}
    )
    return jsonify({"access_token": new_access}), 200
