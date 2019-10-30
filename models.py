from app import db

class Location(db.Model):
    __tablename__ = 'location_db'

    id = db.Column(db.Integer, primary_key=True)
    longitude = db.Column(db.String())
    latitude = db.Column(db.String())
    datetime = db.Column(db.String())

    def __init__(self, longitude, latitude, datetime):
        self.longitude = longitude
        self.latitude = latitude
        self.datetime = datetime

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id, 
            'longitude': self.longitude,
            'latitude': self.latitude,
            'datetime':self.datetime
        }