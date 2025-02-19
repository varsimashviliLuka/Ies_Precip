from src.extensions import db
from src.models.base import BaseModel


class Stations(db.Model, BaseModel):
    __tablename__ = 'stations'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    station_name = db.Column(db.String(256), nullable=False)
    url = db.Column(db.String(512), nullable=False)
    api = db.Column(db.String(512), nullable=False)
    latitude = db.Column(db.Numeric(9, 6), nullable=False)
    longitude = db.Column(db.Numeric(9, 6), nullable=False)


    map_status = db.Column(db.Boolean,default=True)  
    fetch_status = db.Column(db.Boolean, default=True)


    # Relationship with WeatherData
    weather_data = db.relationship('WeatherData', back_populates='stations')
    prev_precip = db.relationship('PrevPrecip', back_populates='stations')

    div_positions = db.relationship('DivPositions', back_populates='stations')

    def __repr__(self):
        return f"<Station(id={self.id}, name={self.station_name})>"
    

class DivPositions(db.Model, BaseModel):
    __tablename__ = 'div_positions'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    station_id = db.Column(db.Integer, db.ForeignKey('stations.id'), nullable=False)
    static_px = db.Column(db.Float, nullable=False)

    left_right = db.Column(db.Float, nullable=False)

    line_rotate = db.Column(db.Float, nullable=False)
    line_left_right = db.Column(db.Float, nullable=False)
    line_top_bottom = db.Column(db.Float, nullable=False)

    shorten_station_name = db.Column(db.String(256), nullable=False)

    map_selected = db.Column(db.Integer, nullable=False)

    first_div_height = db.Column(db.Float, nullable=False)

    precip_accum = db.Column(db.String(20), nullable=False)
    precip_rate = db.Column(db.String(20), nullable=False)
    precip_accum_long = db.Column(db.String(20), nullable=False)

    top_bottom = db.Column(db.Float, nullable=False)

    # Relationship with WeatherData
    stations = db.relationship('Stations', back_populates='div_positions')

    def __repr__(self):
        return f"<Station(id={self.id}, name={self.station_id})>"