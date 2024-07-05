
from aldo.extensions import db

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    contact = db.Column(db.String(20))

    # Define the relationship with Notification model
    notifications = db.relationship('Notification', back_populates='recipient', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'
