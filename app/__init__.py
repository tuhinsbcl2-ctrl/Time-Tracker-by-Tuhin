from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_name='development'):
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    
    from app.auth import auth_bp
    from app.main import main_bp
    from app.tasks import tasks_bp
    from app.timers import timers_bp
    from app.dashboards import dashboards_bp
    from app.reports import reports_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(timers_bp)
    app.register_blueprint(dashboards_bp)
    app.register_blueprint(reports_bp)
    
    with app.app_context():
        db.create_all()
    
    return app
