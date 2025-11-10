# app/models/__init__.py
from app.extensions import db, ma
from .user import User, UserSchema
from .service import Service
from .payment import Payment

__all__ = ["User","UserSchema", "Payment", "Service", "db", "ma"]
