

from datetime import datetime
from aldo.extensions import db

class Payment(db.Model):
    __tablename__ = 'payments'

    payment_id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.booking_id'), nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    amount = db.Column(db.Float)
    payment_method = db.Column(db.String(50))
    status = db.Column(db.String(20))

    booking = db.relationship('Booking', backref='payments')

    def __repr__(self):
        return f'<Payment {self.payment_id}>'
