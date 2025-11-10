from datetime import datetime
from app.extensions import db, ma

class Service(db.Model):
    __tablename__ = "services"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False, default=0.0)
    category = db.Column(db.String(80), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # ✅ Explicit constructor so Pylance recognizes these fields
    def __init__(self, name: str, description: str = None,
                 price: float = 0.0, category: str = None):
        self.name = name
        self.description = description
        self.price = price
        self.category = category

    def __repr__(self):
        return f"<Service {self.name}>"

class ServiceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Service
        load_instance = True
