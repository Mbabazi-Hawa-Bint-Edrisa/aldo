from flask import Flask
from aldo.extensions import db, migrate, jwt, bcrypt
from aldo.controllers.booking_controller import booking_bp 
from aldo.controllers.payments_controller import payment_bp
from aldo.controllers.notifications_controller import notification_bp
from aldo.controllers.t_package_controller import travel_package_bp
from aldo.controllers.user_accounts_controller import user_bp
from aldo.controllers.dashboard_controller import admin_bp


def create_app():
    app = Flask(__name__)

    # Load configuration from config.py
    app.config.from_object('config.Config')

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)

    # Register blueprints
    app.register_blueprint(booking_bp, url_prefix='/api/v1/booking')
    app.register_blueprint(notification_bp, url_prefix='/api/v1/notification')
    app.register_blueprint(payment_bp, url_prefix='/api/v1/payment')
    app.register_blueprint(travel_package_bp, url_prefix='/api/v1/travel_package')
    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(admin_bp, url_prefix='/api/admin') 
 

    return app
