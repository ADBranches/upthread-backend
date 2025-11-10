from datetime import datetime
from app.extensions import db, ma

class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    service_id = db.Column(db.Integer, db.ForeignKey("services.id"))
    amount = db.Column(db.Numeric(10,2), nullable=False)
    status = db.Column(db.String(30), default="pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref="payments")
    service = db.relationship("Service", backref="payments")

class PaymentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Payment
        load_instance = True
