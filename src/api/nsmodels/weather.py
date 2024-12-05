from flask_restx import reqparse, fields
from src.extensions import api



weather_ns = api.namespace('Weather', description='API endpoint for Station related operations', path='/api')


weather_model = weather_ns.model('weather', {
    'id': fields.Integer(required=True, description='Project id', example=1),
    'station_id': fields.Integer(required=True, description='The ID of the related project'),
    'precip_rate': fields.String(required=False, description='Contract number', example='1A2345'),
    'precip_accum': fields.String(required=False, description='Contractor', example='New Contractor'),
    'precip_time': fields.DateTime(required=True, description='Start time (YYYY-MM-DD)', example='2024-01-23')
})


weather_parser = reqparse.RequestParser()

weather_parser.add_argument("weather_name", required=True, type=str, help="Project name example: AKHN Project")

