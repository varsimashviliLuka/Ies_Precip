from flask_restx import reqparse, fields
from src.extensions import api

filter_ns = api.namespace('Filters', description='API endpoint for Filters related operations', path='/api')

filter_model = filter_ns.model('Filters', {
    'id': fields.Integer(required=True, description='Weather data ID', example=1),
    'station_id': fields.Integer(required=True, description='Station ID', example=1),
    'precip_rate': fields.String(required=False, description='Precipitation rate', example='1.19'),
    'precip_accum': fields.String(required=False, description='Precipitation accumulation', example='0.25'),
    'precip_time': fields.DateTime(required=True, description='Event time (YYYY-MM-DD HH:MM:SS)', example='2024-01-23 10:25:03')
})


filter_parser = reqparse.RequestParser()

filter_parser.add_argument("station_id",required=True, type=int, help="Please enter station ID")
filter_parser.add_argument("date",required=True, type=str, help="Please enter date")
filter_parser.add_argument('start_time',required=True, type=str, help="Please enter start time")
filter_parser.add_argument('end_time',required=True, type=str, help="Please enter end time")
filter_parser.add_argument('step_min',required=True, type=int, help="Please enter steps in minutes")
