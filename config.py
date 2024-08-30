# import os

# class Config:
#     ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recess_project'
#     SECRET_KEY = os.getenv('SECRET_KEY', 'safaris')
#     MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
#     MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
#     MAIL_USERNAME = os.getenv('MAIL_USERNAME')
#     MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
#     MAIL_USE_TLS = bool(int(os.getenv('MAIL_USE_TLS', 2)))  # Converts '1' to True, '0' to False
#     MAIL_USE_SSL = bool(int(os.getenv('MAIL_USE_SSL', 1)))  # Converts '1' to True, '0' to False
#     MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'default_sender@example.com')
import os

class Config:
    # Correctly define the database URI as a class attribute
    SQLALCHEMY_DATABASE_URI = 'sqlite:///recess_project'
    
    # Set the secret key and other configurations
    SECRET_KEY = os.getenv('SECRET_KEY', 'safaris')
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    
    # Convert environment variables to booleans
    MAIL_USE_TLS = bool(int(os.getenv('MAIL_USE_TLS', 1)))  # '1' is True, '0' is False
    MAIL_USE_SSL = bool(int(os.getenv('MAIL_USE_SSL', 0)))  # '1' is True, '0' is False
    
    # Default sender for emails
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'default_sender@example.com')
