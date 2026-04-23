from flask import Flask
from .common import Config, db
from .common.mail_utils import mail
from flask_apscheduler import APScheduler

from flask_login import LoginManager
from .common.auth_utils import load_user_callback

scheduler = APScheduler()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, 
                template_folder='ui/templates', 
                static_folder='ui/static')
    app.config.from_object(Config)

    # Initialize components
    db.init_app(app)
    mail.init_app(app)
    scheduler.init_app(app)
    
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.user_loader(load_user_callback)
    
    # Registration of scheduled tasks
    from .common.tasks import check_and_send_reminders
    scheduler.add_job(id='billing_reminder', func=check_and_send_reminders, trigger='cron', hour=9, minute=0, args=[app])
    
    scheduler.start()

    with app.app_context():
        from .sql import schema
        from sqlalchemy import text
        for statement in schema.CREATE_TABLE_STATEMENTS:
            db.session.execute(text(statement))
        db.session.commit()

    # Register blueprints
    from .handler.dashboard_handler import main_bp
    from .handler.auth_handler import auth_bp
    from .handler.user_handler import user_bp
    from .handler.society_handler import society_bp
    from .handler.house_handler import house_bp
    from .handler.billing_handler import maintenance_bp
    from .handler.complaint_handler import complaint_bp
    from .handler.expense_handler import expense_bp

    app.register_blueprint(main_bp, url_prefix="/")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(user_bp, url_prefix="/users")
    app.register_blueprint(society_bp, url_prefix="/societies")
    app.register_blueprint(house_bp, url_prefix="/houses")
    app.register_blueprint(maintenance_bp, url_prefix="/billing")
    app.register_blueprint(complaint_bp, url_prefix="/complaints")
    app.register_blueprint(expense_bp, url_prefix="/expenses")

    @app.route('/ui/uploads/<path:filename>')
    def uploaded_file(filename):
        from flask import send_from_directory
        return send_from_directory(os.path.join(app.root_path, 'ui', 'uploads'), filename)

    return app
