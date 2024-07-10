
# from datetime import datetime
# from aldo.extensions import db

# class Notification(db.Model):
#     __tablename__ = 'notifications'

#     notification_id = db.Column(db.Integer, primary_key=True)
#     recipient_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
#     message = db.Column(db.Text)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     status = db.Column(db.String(20))

#     # Define the relationship with User model
#     recipient = db.relationship('User', back_populates='notifications')

#     def __repr__(self):
#         return f'<Notification {self.notification_id} to User {self.recipient_id}>'
from datetime import datetime
from aldo.extensions import db

class Notification(db.Model):
    __tablename__ = 'notifications'

    notification_id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20))

    def __repr__(self):
        return f'<Notification {self.notification_id}>'
