from flask_restx import Resource

from src.api.nsmodels import stations_ns, stations_model, stations_parser
from src.models import Stations


@stations_ns.route('/stations')
@stations_ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 401: 'JWT Token Expires', 403: 'Unauthorized', 404: 'Not Found'})
class StationsListAPI(Resource):
    @stations_ns.marshal_with(stations_model)
    def get(self):
        '''წამოვიღოთ ყველა სადგურების ინფორმაცია'''
        
        stations = Stations.query.all()
        if not stations:
            return {"error": "სადგურები არ მოიძებნა."}, 404
        
        return stations, 200
    @stations_ns.marshal_with(stations_model)
    @stations_ns.doc(parser=stations_parser)
    def put(self):
        '''ახალი სადგურის დამატება'''

        args = stations_parser.parse_args()


        try:
            latitude = args.get('latitude')
        except ValueError:
            return {"error": "ფორმატის არასწორი ტიპი. გამოიყენეთ ციფრი/რიცხვი"}, 400
        

        try:
            longitude = args.get('longitude')
        except ValueError:
            return {"error": "ფორმატის არასწორი ტიპი. გამოიყენეთ ციფრი/რიცხვი"}, 400
        

        new_station = Stations(station_name = args['station_name'],
                               url = args['url'],
                               api = args['api'],
                               latitude = latitude,
                               longitude = longitude)
        
        new_station.create()
        return new_station, 200
    
@stations_ns.route('/stations/<int:id>')
@stations_ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 401: 'JWT Token Expires', 403: 'Unauthorized', 404: 'Not Found'})
class StationsAPI(Resource):

    @stations_ns.marshal_with(stations_model)
    def post(self,id):
        '''წამოვიღოთ კონკრეტული სადგურის ინფორმაცია'''

        station = Stations.query.filter_by(id=id).first()
        if not station:
            return {"error": "სადგურები არ მოიძებნა."}, 404
        
        return station, 200
    
    def delete(self,id):
        '''კონკრეტული სადგურის წაშლა'''

        station = Stations.query.filter_by(id=id).first()
        if not station:
            return {"error": "სადგური არ მოიძებნა."}, 404
        station.delete()
        return {"message": "სადგური წარმატებით წაიშალა."}, 200
    
