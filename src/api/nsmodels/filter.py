from flask_restx import reqparse, fields
from src.extensions import api

filter_ns = api.namespace('Filters', description='API endpoint for Filters related operations', path='/api')

filter_model = filter_ns.model('Filters', {
    'id': fields.Integer(required=True, description='Project id', example=1),
    'station_id': fields.Integer(required=True, description='The ID of the related project'),
    'precip_rate': fields.String(required=False, description='Contract number', example='1A2345'),
    'precip_accum': fields.String(required=False, description='Contractor', example='New Contractor'),
    'precip_time': fields.DateTime(required=True, description='Start time (YYYY-MM-DD)', example='2024-01-23')
})

def empty_or_none(value):
    if value == "":
        return None
    return str(value)


filter_parser = reqparse.RequestParser()

filter_parser.add_argument("station_id", type=empty_or_none, help="Please enter station ID")
filter_parser.add_argument("start_time",required=True, type=str, help="Please enter start date")
filter_parser.add_argument('end_time',required=True, type=str, help="Please enter end date")
filter_parser.add_argument('step_hour', type=int, help="Please enter step (hour)")
