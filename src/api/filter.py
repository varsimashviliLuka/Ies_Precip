from flask_restx import Resource
from datetime import datetime
from sqlalchemy import and_, func
from sqlalchemy.sql import extract

from src.api.nsmodels import filter_ns, filter_parser, filter_model
from src.models import WeatherData


@filter_ns.route('/filter')
@filter_ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 401: 'JWT Token Expires', 403: 'Unauthorized', 404: 'Not Found'})
class FilterAPI(Resource):
    @filter_ns.doc(parser=filter_parser)
    @filter_ns.marshal_with(filter_model)
    def post(self):
        '''გავფილტროთ პროექტები სხვადასხვა პარამეტრებით'''
        # Parse the filter arguments
        args = filter_parser.parse_args()

        # Extract filter parameters

        try:
            date = datetime.strptime(args['date'], '%Y-%m-%d').date()
        except ValueError:
            return {"error": "ფორმატის არასწორი ტიპი. გამოიყენეთ YYYY-MM-DD."}, 400
        try:
            start_time = datetime.strptime(args['start_time'], '%H:%M:%S').time()
        except ValueError:
            return {"error": "ფორმატის არასწორი ტიპი. გამოიყენეთ HH-MM-SS."}, 400
        try:
            end_time = datetime.strptime(args['end_time'], '%H:%M:%S').time()
        except ValueError:
            return {"error": "ფორმატის არასწორი ტიპი. გამოიყენეთ HH-MM-SS."}, 400
        try:
            step_min = int(args.get('step_min'))
        except ValueError:
            return {"error": "ფორმატის არასწორი ტიპი. გამოიყენეთ ციფრი/რიცხვი"}, 400
        try:
            station_id = int(args.get('station_id'))
        except ValueError:
            return {"error": "ფორმატის არასწორი ტიპი. გამოიყენეთ ციფრი/რიცხვი"}, 400
        
        if step_min % 5 != 0:
            return {"error": "დარწმუნდით, რომ მითითებული სტეპი იყოფა 5-ზე"}, 400

        weather_data = WeatherData.query.filter(WeatherData.station_id==station_id,
                                            func.date(WeatherData.precip_time) == date,
                                            func.time(WeatherData.precip_time) >= start_time,
                                            func.time(WeatherData.precip_time) <= end_time,
                                            (extract('hour',WeatherData.precip_time) * 60 + extract('minute',WeatherData.precip_time)) % step_min == 0
                                            ).all()
        if not weather_data:
            return {"error": "მონაცემი ვერ მოიძებნა"}, 404

        

        return weather_data, 200
        




        