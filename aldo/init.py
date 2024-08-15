from flask import Flask
from flask_mail import Mail
from aldo.extensions import db, migrate, jwt, bcrypt
from aldo.controllers.booking_controller import booking_bp 
from aldo.controllers.message_controller import message
from aldo.controllers.t_package_controller import travel_package_bp
from aldo.controllers.user_accounts_controller import user_bp
from aldo.controllers.dashboard_controller import dashboard_bp
from flask_cors import CORS
from dotenv import load_dotenv
import os

mail = Mail()

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Load environment variables
    load_dotenv()

    # Load configuration from config.py
    app.config.from_object('config.Config')

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    
    
     # Configure CORS
    CORS(app, resources={r"/api/*": {"origins": "https://github.com/Mbabazi-Hawa-Bint-Edrisa/projectAldo.git"}})

    # Register blueprints
    app.register_blueprint(booking_bp, url_prefix='/api/v1/booking')
    app.register_blueprint(message, url_prefix='/api/v1/message')
    app.register_blueprint(travel_package_bp, url_prefix='/api/v1/travel_package')
    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(dashboard_bp, url_prefix='/api/admin')

    return app

# from flask import Flask
# from flask_mail import Mail
# from aldo.extensions import db, migrate, jwt, bcrypt
# from aldo.controllers.booking_controller import booking_bp 
# # from aldo.controllers.payments_controller import payment_bp
# from aldo.controllers.message_controller import message
# from aldo.controllers.t_package_controller import travel_package_bp
# from aldo.controllers.user_accounts_controller import user_bp
# from aldo.controllers.dashboard_controller import dashboard_bp
# from flask_cors import CORS
# import os

# class Config:
#     SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
#     SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///your_database.db')
#     MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
#     MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
#     MAIL_USERNAME = os.getenv('MAIL_USERNAME')
#     MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
#     MAIL_USE_TLS = bool(os.getenv('MAIL_USE_TLS', True))
#     MAIL_USE_SSL = bool(os.getenv('MAIL_USE_SSL', False))
#     MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'default_sender@example.com')


# mail = Mail()

# def create_app():
#     app = Flask(__name__)
#     CORS(app)

#     # Load configuration from config.py
#     app.config.from_object('config.Config')

#     # Flask-Mail configuration
#     # app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Or your email provider's SMTP server
#     # app.config['MAIL_PORT'] = 587
#     # app.config['MAIL_USERNAME'] = 'hawambabazi500@gmail.com'  # Your email address
#     # app.config['MAIL_PASSWORD'] = 'edrisa1234'  # Your email password
#     # app.config['MAIL_USE_TLS'] = True
#     # app.config['MAIL_USE_SSL'] = False
#     # app.config['MAIL_DEFAULT_SENDER'] = 'hawambabazi500@gmail.com'
   

# class Config:
#     SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
#     SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///your_database.db')
#     MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
#     MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
#     MAIL_USERNAME = os.getenv('MAIL_USERNAME')
#     MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
#     MAIL_USE_TLS = bool(os.getenv('MAIL_USE_TLS', True))
#     MAIL_USE_SSL = bool(os.getenv('MAIL_USE_SSL', False))
#     MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'default_sender@example.com')


#     # Initialize extensions
#     db.init_app(app)
#     migrate.init_app(app, db)
#     jwt.init_app(app)
#     bcrypt.init_app(app)
#     mail.init_app(app)

#     # Register blueprints
#     app.register_blueprint(booking_bp, url_prefix='/api/v1/booking')
#     app.register_blueprint(message, url_prefix='/api/v1/message')
#     # app.register_blueprint(payment_bp, url_prefix='/api/v1/payment')
#     app.register_blueprint(travel_package_bp, url_prefix='/api/v1/travel_package')
#     app.register_blueprint(user_bp, url_prefix='/api')
#     app.register_blueprint(dashboard_bp, url_prefix='/api/admin')

#     return app
