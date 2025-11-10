from flask import Blueprint, request, jsonify
from app.models import Service, db
from app.extensions import ma
from app.utils.auth_utils import role_required
from flask_jwt_extended import jwt_required
from app.models.service import ServiceSchema, Service

service_bp = Blueprint("services", __name__, url_prefix="/api/v1/services")

service_schema = ServiceSchema()
services_schema = ServiceSchema(many=True)

# 🔹 List all services
@service_bp.get("/")
def list_services():
    query = Service.query
    category = request.args.get("category")
    search = request.args.get("search")
    if category:
        query = query.filter(Service.category.ilike(f"%{category}%"))
    if search:
        query = query.filter(Service.name.ilike(f"%{search}%"))
    return services_schema.jsonify(query.all()), 200

# 🔹 Create service (admin only)
@service_bp.post("/")
@role_required("admin")
def create_service():
    data = request.get_json() or {}
    new_service = Service(
        name=data.get("name"),
        description=data.get("description"),
        price=data.get("price", 0.0),
        category=data.get("category"),
    )
    db.session.add(new_service)
    db.session.commit()
    return service_schema.jsonify(new_service), 201

# 🔹 Retrieve one
@service_bp.get("/<int:id>")
def get_service(id):
    service = Service.query.get_or_404(id)
    return service_schema.jsonify(service)

# 🔹 Update (admin)
@service_bp.put("/<int:id>")
@role_required("admin")
def update_service(id):
    service = Service.query.get_or_404(id)
    data = request.get_json() or {}
    for field in ["name", "description", "price", "category"]:
        if field in data:
            setattr(service, field, data[field])
    db.session.commit()
    return service_schema.jsonify(service)

# 🔹 Delete (admin)
@service_bp.delete("/<int:id>")
@role_required("admin")
def delete_service(id):
    service = Service.query.get_or_404(id)
    db.session.delete(service)
    db.session.commit()
    return jsonify({"message": "Service deleted"}), 204
