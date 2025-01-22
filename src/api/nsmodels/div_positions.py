from flask_restx import reqparse, fields, inputs
from src.extensions import api


div_positions_ns = api.namespace('Stations Div Positions', description='API სადგურების div პოზიციების შესახებ', path='/api')


div_positions_model = div_positions_ns.model('Div Positions', {
    'PRECIP_ACCUM': fields.String(required=True, description='აკუმულაცია', example='0.99'),
    'PRECIP_RATE': fields.String(required=True, description='ინტენსივობა', example='0.00'),
    'PRECIP_ACCUM_LONG': fields.String(required=True, description='გრძელი აკუმულაცია', example='0.00'),
    'Station': fields.String(required=True, description='სადგურის სახელი', example='2902 Rioni - IGUMAT4'),
    'Url': fields.String(required=True, description='სადგურის Url', example='https://www.wunderground.com/dashboard/pws/IGUMAT4'),
    'api': fields.String(required=True, description='სადგურის API', example='https://api.weather.com/v2/pws/observations/current?apiKey=e1f10a1e78da46f5b10a1e78da....'),
    'first_div_height': fields.Float(required=True, description='first_div_height', example=0.99),

    'id': fields.String(required=True, description='id', example='IGUMAT4'),
    
    'latitude': fields.Float(required=True, description='სადგურის განედი', example=42.33),
    'left_right': fields.Float(required=True, description='left_right', example=-5),
    'line_left_right': fields.Float(required=True, description='line_left_right', example=-6),
    'line_rotate': fields.Float(required=True, description='line_rotate', example=-45),
    'line_top_bottom': fields.Float(required=True, description='line_top_bottom', example=-13),
    'longitude': fields.Float(required=True, description='სადგურის გრძედი', example=42.69),
    'static_px': fields.Float(required=True, description='static_px', example=-45),
    'map_status': fields.Float(required=True, description='map_status', example=0),
    'top_bottom': fields.Float(required=True, description='top_bottom', example=-45.99),
})


