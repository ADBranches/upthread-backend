from flask import Flask
from dotenv import load_dotenv
import os

from app.extensions import db, jwt, bcrypt, cors, migrate, ma
from app.auth.routes import auth_bp
from app.routes.protected import protected_bp  # we'll create this
from app.routes.service_routes import service_bp

from datetime import timedelta

def create_app():
    load_dotenv()
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

    access_secs = int(os.getenv("ACCESS_TOKEN_EXPIRES", "3600"))
    refresh_secs = int(os.getenv("REFRESH_TOKEN_EXPIRES", "86400"))
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(seconds=access_secs)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(seconds=refresh_secs)
    
    # initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(protected_bp)
    app.register_blueprint(service_bp)

    return app
