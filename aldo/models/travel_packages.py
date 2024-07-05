
# from aldo.extensions import db

# class TravelPackage(db.Model):
#     __tablename__ = 'travel_packages'

#     package_id = db.Column(db.Integer, primary_key=True)
#     package_name = db.Column(db.String(100), nullable=False)
#     description = db.Column(db.Text)
#     destinations = db.Column(db.Text(255))
#     activities = db.Column(db.Text(255))
#     inclusions = db.Column(db.Text)
#     price = db.Column(db.Float)
#     duration = db.Column(db.Integer)
#     availability = db.Column(db.Boolean)
#     image_url = db.Column(db.String(200))

#     def __repr__(self):
#         return f'<TravelPackage {self.package_name}>'
from aldo.extensions import db
import json

class TravelPackage(db.Model):
    __tablename__ = 'travel_packages'

    package_id = db.Column(db.Integer, primary_key=True)
    package_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    destinations = db.Column(db.Text)  # Use Text for JSON strings
    activities = db.Column(db.Text)  # Use Text for JSON strings
    inclusions = db.Column(db.Text)  # Use Text for JSON strings
    price = db.Column(db.Float)
    duration = db.Column(db.Integer)
    availability = db.Column(db.Boolean)
    image_url = db.Column(db.String(200))

    def __repr__(self):
        return f'<TravelPackage {self.package_name}>'

    @property
    def destinations_list(self):
        return json.loads(self.destinations) if self.destinations else []

    @destinations_list.setter
    def destinations_list(self, value):
        self.destinations = json.dumps(value)

    @property
    def activities_list(self):
        return json.loads(self.activities) if self.activities else []

    @activities_list.setter
    def activities_list(self, value):
        self.activities = json.dumps(value)

    @property
    def inclusions_list(self):
        return json.loads(self.inclusions) if self.inclusions else []

    @inclusions_list.setter
    def inclusions_list(self, value):
        self.inclusions = json.dumps(value)
