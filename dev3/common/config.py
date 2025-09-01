import os
from flask import Flask
from dev3.common.db_connection import db
from dotenv import load_dotenv

load_dotenv()  # load .env file

def create_app():
    app = Flask(__name__, 
                template_folder="dev3/ui/templates", 
                static_folder="dev3/ui/static")

    # Config
    app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET", "fallback_secret")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Init DB
    db.init_app(app)

    # Register Blueprints
    from dev3.handlers.user_handler import user_bp
    from dev3.handlers.bill_handler import bill_bp
    from dev3.handlers.complaint_handler import complaint_bp
    from dev3.handlers.event_handler import event_bp

    app.register_blueprint(user_bp, url_prefix="/users")
    app.register_blueprint(bill_bp, url_prefix="/bills")
    app.register_blueprint(complaint_bp, url_prefix="/complaints")
    app.register_blueprint(event_bp, url_prefix="/events")

    return app
