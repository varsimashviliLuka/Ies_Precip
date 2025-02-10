from flask_restx import Resource
from datetime import datetime
from sqlalchemy import func

from flask_jwt_extended import jwt_required

from src.api.nsmodels import export_ns, export_parser
from src.models import WeatherData
from src.config import Config

import csv
import os



@export_ns.route('/export')
@export_ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 401: 'JWT Token Expires', 403: 'Unauthorized', 404: 'Not Found'})
class Export_API(Resource):
    @jwt_required()
    @export_ns.doc(security="JsonWebToken")
    @export_ns.doc(parser=export_parser)
    def post(self):
        '''გავფილტროთ მონაცემები სხვადასხვა პარამეტრებით'''
        # Parse the filter arguments
        args = export_parser.parse_args()

        try:
            date = datetime.strptime(args['date'], '%Y-%m-%d').date()
        except ValueError:
            return {"error": "ფორმატის არასწორი ტიპი. გამოიყენეთ YYYY-MM-DD."}, 400
        try:
            start_time = datetime.strptime(args['start_time'], '%H:%M:%S').time()
        except ValueError:
            return {"error": "ფორმატის არასწორი ტიპი. გამოიყენეთ HH:MM:SS."}, 400
        try:
            end_time = datetime.strptime(args['end_time'], '%H:%M:%S').time()
        except ValueError:
            return {"error": "ფორმატის არასწორი ტიპი. გამოიყენეთ HH:MM:SS."}, 400
        try:
            step_min = int(args.get('step_min'))
        except ValueError:
            return {"error": "ფორმატის არასწორი ტიპი. გამოიყენეთ ციფრი/რიცხვი"}, 400
        try:
            station_id = int(args.get('station_id'))
        except ValueError:
            return {"error": "ფორმატის არასწორი ტიპი. გამოიყენეთ ციფრი/რიცხვი"}, 400
        
        response_format = args.get('format', 'json')
        
        if step_min % 5 != 0:
            return {"error": "დარწმუნდით, რომ მითითებული სტეპი იყოფა 5-ზე"}, 400

        weather_data = WeatherData.query.filter(WeatherData.station_id == station_id,
                                            func.date(WeatherData.precip_time) == date,
                                            func.time(WeatherData.precip_time) >= start_time,
                                            func.time(WeatherData.precip_time) <= end_time).all()
        
        if not weather_data:
            return {"error": "მონაცემი ვერ მოიძებნა"}, 404

        step = int(step_min / 5)
        filter_data = [weather_data[i] for i in range(0, len(weather_data), step)]

        # Create a unique filename for each request
        file_name = f"{str(date)}.csv"
        file_path = os.path.join(Config.EXPORT_DIR, file_name)

        # Create a CSV file and write the filtered data
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ["id", "station_id", "precip_time", "precip_rate", "precip_accum", "precip_accum_long"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write the header
            writer.writeheader()

            # Write each row of data as a dictionary
            for data in filter_data:
                writer.writerow({
                    "id": data.id,
                    "station_id": data.station_id,
                    "precip_time": data.precip_time,
                    "precip_rate": data.precip_rate,
                    "precip_accum": data.precip_accum,
                    "precip_accum_long": data.precip_accum_long
                })

        # Respond with the file path or URL to access the file
        export_url = f'/export/{file_name}'  # The URL to download the file
        return export_url, 200
