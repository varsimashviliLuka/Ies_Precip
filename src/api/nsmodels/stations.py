from flask_restx import reqparse, fields
from src.extensions import api



stations_ns = api.namespace('Stations', description='API endpoint for Station related operations', path='/api')


stations_model = stations_ns.model('Stations', {
    'id': fields.Integer(required=True, description='Project id', example=1),
    'station_name': fields.String(required=True, description='Project name', example='New Project'),
    'url': fields.String(required=False, description='Contract number', example='1A2345'),
    'api': fields.String(required=False, description='Contractor', example='New Contractor'),
    'latitude': fields.Float(required=True, description='Project latitude', example=42.0163),
    'longitude': fields.Float(required=True, description='Project longitude', example=43.1412),
})


stations_parser = reqparse.RequestParser()

stations_parser.add_argument("stations_name", required=True, type=str, help="Project name example: AKHN Project")

