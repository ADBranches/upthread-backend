import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
from app import create_app
from app.extensions import db

def create_test_app():
    app = create_app()
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        WTF_CSRF_ENABLED=False,
    )
    with app.app_context():
        db.create_all()
    return app

def test_register_and_login():
    app = create_test_app()
    client = app.test_client()

    # Register
    resp = client.post("/api/v1/auth/register", json={
        "email": "pytest@example.com",
        "password": "123456",
        "role": "admin"
    })
    assert resp.status_code in (201, 409)  # if run twice user may exist

    # Login
    resp = client.post("/api/v1/auth/login", json={
        "email": "pytest@example.com",
        "password": "123456",
    })
    assert resp.status_code == 200
    data = resp.get_json()
    assert "access_token" in data

    token = data["access_token"]

    # /me protected route
    resp = client.get("/api/v1/me", headers={
        "Authorization": f"Bearer {token}"
    })
    assert resp.status_code == 200
    me = resp.get_json()
    assert me["email"] == "pytest@example.com"

