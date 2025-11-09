from flask import Flask
from flask_cors import CORS
from app.extensions import db, ma
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    db.init_app(app)
    ma.init_app(app)

    # Blueprints placeholders
    from app.routes import register_blueprints
    register_blueprints(app)

    return app
