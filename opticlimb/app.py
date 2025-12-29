from flask import Flask

from .model import db
from .view import main_bp

def create_app():
    app = Flask(__name__)
    app.config.from_envvar('OPTICLIMB_CONFIG')

    db.init_app(app)
    app.register_blueprint(main_bp)

    return app
