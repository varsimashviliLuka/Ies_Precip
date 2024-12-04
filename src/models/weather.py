from src.extensions import db
from src.models.base import BaseModel


class WeatherData(db.Model):
    __tablename__ = 'weather_data'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    station_id = db.Column(db.Integer, db.ForeignKey('stations.id'), nullable=False)
    precip_rate = db.Column(db.String(128), nullable=False)
    precip_accum = db.Column(db.String(128), nullable=False)
    precip_time = db.Column(db.DateTime, nullable=False)


    def __repr__(self):
        return f"<WeatherData(id={self.id}, station_id={self.station_id}, precip_rate={self.precip_rate})>"