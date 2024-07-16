from datetime import datetime
from aldo.extensions import db

class Booking(db.Model):
    __tablename__ = 'bookings'

    booking_id = db.Column(db.Integer, primary_key=True)
    package_id = db.Column(db.Integer, db.ForeignKey('travel_packages.package_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    date_of_booking = db.Column(db.DateTime, default=datetime.utcnow)
    travel_start_date = db.Column(db.Date)  # Linked with TravelPackage
    travel_end_date = db.Column(db.Date)  # Linked with TravelPackage
    total_cost = db.Column(db.Float)
    payment_status = db.Column(db.String(20))
    booking_status = db.Column(db.String(20))
    transportation = db.Column(db.String(100))
    booking_source = db.Column(db.String(20))

    # Relationships
    user = db.relationship('User', backref='bookings')
    package = db.relationship('TravelPackage')

    def __repr__(self):
        return f'<Booking {self.booking_id}>'
