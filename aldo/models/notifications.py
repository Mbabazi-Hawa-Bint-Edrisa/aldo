from aldo.extensions import db

class Notification(db.Model):
    __tablename__ = 'notifications'

    notification_id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text)

    def __repr__(self):
        return f'<Notification {self.notification_id}>'

