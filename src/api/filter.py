from flask_restx import Resource
from datetime import datetime
from sqlalchemy import and_

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
        station_id = args.get('station_id')
        step_hour = args.get('step_hour')


        try:
            start_time = datetime.strptime(args['start_time'], '%Y-%m-%d %H:%M:%S.%f')
        except ValueError:
            return {"error": "ფორმატის არასწორი ტიპი. გამოიყენეთ YYYY-MM-DD."}, 400

        try:
            end_time = datetime.strptime(args['end_time'], '%Y-%m-%d %H:%M:%S.%f')
        except ValueError:
            return {"error": "ფორმატის არასწორი ტიპი. გამოიყენეთ YYYY-MM-DD."}, 400
        print(station_id)
        if station_id is None:
            weather_data = WeatherData.query.filter(WeatherData.precip_time.between(start_time,end_time)).all()
        
        return weather_data, 200
        


        