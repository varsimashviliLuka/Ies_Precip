from flask_restx import reqparse, fields, inputs
from src.extensions import api


stations_ns = api.namespace('Stations', description='API სადგურების შესახებ', path='/api')


stations_model = stations_ns.model('Stations', {
    'id': fields.Integer(required=True, description='სადგურის ID', example=1),
    'station_name': fields.String(required=True, description='სადგურის სახელი', example='Bazaleti - IUNDILAA2'),
    'url': fields.String(required=False, description='Wunderground-ის ლინკი', example='https://www.wunderground.com/dashboard/pws/IUNDILAA2'),
    'api': fields.String(required=False, description='Wunderground api-ის ლინკი', example='https://api.weather.com/v2/pws/observations/current?apiKey=e1f10a1e7..'),
    'latitude': fields.Float(required=True, description='სადგურის განედი', example=42.0163),
    'longitude': fields.Float(required=True, description='სადგურის გრძედი', example=43.1412),
    'status': fields.Boolean(required=True,description='სადგურის სტატუს',example=True)
})


stations_parser = reqparse.RequestParser()

stations_parser.add_argument("station_name", required=True, type=str, help="შეიყვანეთ სადგურის სახელი")
stations_parser.add_argument("url", required=True, type=str, help="შეიყვანეთ სადგურის wunderground-ის ლინკი")
stations_parser.add_argument("api", required=True, type=str, help="შეიყვანეთ სადგურის wunderground-ის API-ის ლინკი")
stations_parser.add_argument("latitude", required=True, type=float, help="შეიყვანეთ განედი")
stations_parser.add_argument("longitude", required=True, type=float, help="შეიყვანეთ გრძედი")
stations_parser.add_argument("status", required=True, type=inputs.boolean, help="შეიყვანეთ სტატუსი")

