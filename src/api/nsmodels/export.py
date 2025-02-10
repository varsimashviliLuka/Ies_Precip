from flask_restx import reqparse
from src.extensions import api

export_ns = api.namespace('Exports', description='API CSV ექპორტის შესახებ', path='/api')

export_parser = reqparse.RequestParser()

export_parser.add_argument("station_id",required=False, type=int, help="გთხოვთ შეიყვანეთ სადგურის ID", default=10)
export_parser.add_argument("date",required=True, type=str, help="გთხოვთ შეიყვანეთ თარიღი",default='2025-02-10')
export_parser.add_argument('start_time',required=True, type=str, help="გთხოვთ შეიყვანეთ საწყისი დრო",default='01:01:01')
export_parser.add_argument('end_time',required=True, type=str, help="გთხოვთ შეიყვანეთ დასრულების დრო",default='23:00:00')
export_parser.add_argument('step_min',required=True, type=int, help="გთხოვთ შეიყვანეთ სტეპი წუთებში",default=10)