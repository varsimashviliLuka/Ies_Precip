from flask_restx import reqparse, fields
from src.extensions import api



stations_ns = api.namespace('Stations', description='API endpoint for Station related operations', path='/api')


stations_model = stations_ns.model('Stations', {
    'id': fields.Integer(required=True, description='Station ID', example=1),
    'station_name': fields.String(required=True, description='Station name', example='Bazaleti - IUNDILAA2'),
    'url': fields.String(required=False, description='Wunderground url', example='https://www.wunderground.com/dashboard/pws/IUNDILAA2'),
    'api': fields.String(required=False, description='Wunderground api url', example='https://api.weather.com/v2/pws/observations/current?apiKey=e1f10a1e7..'),
    'latitude': fields.Float(required=True, description='Station latitude', example=42.0163),
    'longitude': fields.Float(required=True, description='Station longitude', example=43.1412),
})


stations_parser = reqparse.RequestParser()

stations_parser.add_argument("stations_name", required=True, type=str, help="Station name example: Bazaleti - IUNDILAA2")

