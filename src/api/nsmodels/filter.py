from flask_restx import reqparse, fields
from src.extensions import api

filter_ns = api.namespace('Filters', description='API ფილტრაციის შესახებ', path='/api')

filter_model = filter_ns.model('Filters', {
    'id': fields.Integer(required=True, description='მონაცემის ID', example=1),
    'station_id': fields.Integer(required=True, description='სადგურის ID', example=10),
    'precip_rate': fields.String(required=False, description='ნალექის მაჩვენებელი', example='1.19'),
    'precip_accum': fields.String(required=False, description='ნალექების დაგროვება', example='0.25'),
    'precip_time': fields.DateTime(required=True, description='მონაცემის თარიღი და დრო(YYYY-MM-DDTHH:MM:SS)', example='2024-06-12T01:30:13')
})


filter_parser = reqparse.RequestParser()

filter_parser.add_argument("station_id",required=True, type=int, help="გთხოვთ შეიყვანეთ სადგურის ID", default=10)
filter_parser.add_argument("date",required=True, type=str, help="გთხოვთ შეიყვანეთ თარიღი",default='2024-06-12')
filter_parser.add_argument('start_time',required=True, type=str, help="გთხოვთ შეიყვანეთ საწყისი დრო",default='01:01:01')
filter_parser.add_argument('end_time',required=True, type=str, help="გთხოვთ შეიყვანეთ დასრულების დრო",default='23:00:00')
filter_parser.add_argument('step_min',required=True, type=int, help="გთხოვთ შეიყვანეთ სტეპი წუთებში",default=10)
