
# from datetime import datetime
# from aldo.extensions import db
# import json

# class Booking(db.Model):
#     __tablename__ = 'bookings'

#     booking_id = db.Column(db.Integer, primary_key=True)
#     package_id = db.Column(db.Integer, db.ForeignKey('travel_packages.package_id'), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
#     date_of_booking = db.Column(db.DateTime, default=datetime.utcnow)
#     travel_start_date = db.Column(db.Date)
#     travel_end_date = db.Column(db.Date)
#     total_cost = db.Column(db.Float)
#     payment_status = db.Column(db.String(20))
#     booking_status = db.Column(db.String(20))
#     destination = db.Column(db.String(100))
#     accommodation = db.Column(db.String(100))
#     transportation = db.Column(db.String(100))
#     activities = db.Column(db.String(255))  # JSON string for activity list
#     booking_source = db.Column(db.String(20))

#     # Relationships
#     user = db.relationship('User', backref='bookings')
#     package = db.relationship('TravelPackage')  # No backref needed here as it's defined in TravelPackage
   

#     @property
#     def activities_list(self):
#         return json.loads(self.activities)

#     @activities_list.setter
#     def activities_list(self, value):
#         self.activities = json.dumps(value)

#     def __repr__(self):
#         return f'<Booking {self.booking_id}>'
from datetime import datetime
from aldo.extensions import db
import json

class Booking(db.Model):
    __tablename__ = 'bookings'

    booking_id = db.Column(db.Integer, primary_key=True)
    package_id = db.Column(db.Integer, db.ForeignKey('travel_packages.package_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    date_of_booking = db.Column(db.DateTime, default=datetime.utcnow)
    travel_start_date = db.Column(db.Date)
    travel_end_date = db.Column(db.Date)
    total_cost = db.Column(db.Float)
    payment_status = db.Column(db.String(20))
    booking_status = db.Column(db.String(20))
    destination = db.Column(db.String(100))
    accommodation = db.Column(db.String(100))
    transportation = db.Column(db.String(100))
    activities = db.Column(db.String(255))  # JSON string for activity list
    booking_source = db.Column(db.String(20))

    # Relationships
    user = db.relationship('User', backref='bookings')
    package = db.relationship('TravelPackage')
    #payments = db.relationship('Payment', backref='bookings')  # Define backref here

    @property
    def activities_list(self):
        return json.loads(self.activities)

    @activities_list.setter
    def activities_list(self, value):
        self.activities = json.dumps(value)

    def __repr__(self):
        return f'<Booking {self.booking_id}>'
