from flask_restx import Resource
from datetime import datetime
from sqlalchemy import func
from flask import send_file
from collections import defaultdict

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
            start_date = datetime.strptime(args['start_date'], '%Y-%m-%d').date()
        except ValueError:
            return {"error": "ფორმატის არასწორი ტიპი. გამოიყენეთ YYYY-MM-DD."}, 400
        try:
            end_date = datetime.strptime(args['end_date'], '%Y-%m-%d').date()
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
            station_ids = [int(x) for x in args['station_ids']]
        except ValueError:
            return {"error": "ფორმატის არასწორი ტიპი. გამოიყენეთ ციფრი/რიცხვი"}, 400

        if step_min % 5 != 0:
            return {"error": "დარწმუნდით, რომ მითითებული სტეპი იყოფა 5-ზე"}, 400
        


        weather_data = WeatherData.query.filter(WeatherData.station_id.in_(station_ids),
                                            func.date(WeatherData.precip_time) >= start_date,
                                            func.date(WeatherData.precip_time) <= end_date,
                                            func.time(WeatherData.precip_time) >= start_time,
                                            func.time(WeatherData.precip_time) <= end_time).order_by(WeatherData.station_id,WeatherData.precip_time).all()
            

        
        if not weather_data:
            return {"error": "მონაცემი ვერ მოიძებნა"}, 404
        

        step = int(step_min / 5)


        grouped_data = defaultdict(list)
        for entry in weather_data:
            grouped_data[entry.station_id].append(entry)

        # Apply step filter within each station's dataset
        filtered_data = []
        for station, data in grouped_data.items():
            filtered_data.extend(data[i] for i in range(0, len(data), step))

        filtered_data.sort(key=lambda x: x.precip_time)


        # Create a unique filename for each request
        file_name = 'export.csv'
        file_path = os.path.join(Config.EXPORT_DIR, file_name)

        # Create a CSV file and write the filtered data
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ["precip_time", "station_name", "precip_rate", "precip_accum", "precip_accum_long"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write the header
            writer.writeheader()

            # Write each row of data as a dictionary
            for data in filtered_data:
                writer.writerow({
                    "precip_time": data.precip_time,
                    "station_name": data.stations.station_name,
                    "precip_rate": data.precip_rate,
                    "precip_accum": data.precip_accum,
                    "precip_accum_long": data.precip_accum_long
                })

        # Respond with the file path or URL to access the file
        try:
            return send_file(file_path, as_attachment=True, download_name=file_name, mimetype='text/csv')
        finally:
            # Ensure that the file is deleted after download
            if os.path.exists(file_path):
                os.remove(file_path)
