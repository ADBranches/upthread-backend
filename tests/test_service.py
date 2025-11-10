import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.extensions import db

def test_service_crud():
    app = create_app()
    app.config.update(TESTING=True, SQLALCHEMY_DATABASE_URI="sqlite://")
    with app.app_context():
        db.create_all()
        client = app.test_client()
        # Public list endpoint works
        res = client.get("/api/v1/services/")
        assert res.status_code == 200
