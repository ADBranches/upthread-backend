from flask import Blueprint

def register_blueprints(app):
    from app.routes.base import base_bp
    app.register_blueprint(base_bp, url_prefix="/api/v1")
