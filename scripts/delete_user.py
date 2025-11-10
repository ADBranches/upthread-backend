# scripts/delete_user.py
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.models import User, db

app = create_app()

with app.app_context():
    email = "kali@gmail.com"
    db.session.query(User).filter_by(email=email).delete()
    db.session.commit()
    print(f"✅ Deleted any user with email={email}")

