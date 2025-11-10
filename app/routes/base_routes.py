from flask import Blueprint, jsonify
from app.models.user import UserSchema
from app.extensions import db
from app.models.user import User

base_bp = Blueprint("base", __name__)

@base_bp.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "message": "Upthread API operational"})

@base_bp.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify(UserSchema(many=True).dump(users))
