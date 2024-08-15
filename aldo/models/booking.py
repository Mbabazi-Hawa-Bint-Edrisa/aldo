from datetime import datetime
from aldo.extensions import db

class Booking(db.Model):
    __tablename__ = 'bookings'

    booking_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    package_id = db.Column(db.Integer, db.ForeignKey('travel_packages.package_id'), nullable=False)
    payment_method = db.Column(db.String(100), nullable=True)
    booking_source = db.Column(db.String(20), nullable=True)
    booking_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    # Relationships
    user = db.relationship('User', backref='bookings', foreign_keys=[user_id])
    package = db.relationship('TravelPackage', backref='bookings', foreign_keys=[package_id])

    def __repr__(self):
        return f'<Booking {self.booking_id}>'

# from datetime import datetime
# from aldo.extensions import db

# class Booking(db.Model):
#     __tablename__ = 'bookings'

#     booking_id = db.Column(db.Integer, primary_key=True)
#     package_id = db.Column(db.Integer, db.ForeignKey('travel_packages.package_id'), nullable=False)
#     payment_method = db.Column(db.String(100), nullable=True)
#     booking_source = db.Column(db.String(20), nullable=True)
#     booking_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

#     # Relationships
#     user = db.relationship('User', backref='bookings', foreign_keys=[user_id])
#     package = db.relationship('TravelPackage', backref='bookings', foreign_keys=[package_id])

#     def __repr__(self):
#         return f'<Booking {self.booking_id}>'
