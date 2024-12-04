from src.extensions import db
from src.models.base import BaseModel


class Station(db.Model):
    __tablename__ = 'stations'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    station_name = db.Column(db.String(256), nullable=False)
    url = db.Column(db.String(512), nullable=False)
    api = db.Column(db.String(512), nullable=False)
    latitude = db.Column(db.Numeric(9, 6), nullable=False)
    longitude = db.Column(db.Numeric(9, 6), nullable=False)

    # Relationship with WeatherData
    weather_data = db.relationship('WeatherData', backref='station', lazy=True)

    def __repr__(self):
        return f"<Station(id={self.id}, name={self.station_name})>"