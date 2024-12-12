from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.api.nsmodels import stations_ns, stations_model, stations_parser
from src.models import Stations, WeatherData, User, Role



@stations_ns.route('/stations')
@stations_ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 401: 'JWT Token Expires', 403: 'Unauthorized', 404: 'Not Found'})
class StationsListAPI(Resource):
    
    @stations_ns.marshal_with(stations_model)
    @jwt_required()
    @stations_ns.doc(security="JsonWebToken")
    def get(self):
        '''წამოვიღოთ ყველა სადგურების ინფორმაცია'''
        
        stations = Stations.query.all()
        if not stations:
            return {"error": "სადგურები არ მოიძებნა."}, 404
        
        return stations, 200
    
    @jwt_required()
    @stations_ns.doc(security="JsonWebToken")
    @stations_ns.doc(parser=stations_parser)
    def post(self):
        '''ახალი სადგურის დამატება'''

        identity = get_jwt_identity()

        admin = User.query.filter_by(uuid=identity).first()
        if not admin.check_permission():
            return {"message": 'თქვენ არ გაქვთ სადგურის დამატების უფლება'}, 403

        args = stations_parser.parse_args()



        new_station = Stations(station_name = args.get('station_name'),
                               url = args.get('url'),
                               api = args.get('api'),
                               latitude = args.get('latitude'),
                               longitude = args.get('longitude'),
                               status=args.get('status'))
        
        new_station.create()

        return {"message": f"სადგური წარმატებით დაემატა. სადგურის ID: {new_station.id}"}, 200
    
@stations_ns.route('/stations/<int:id>')
@stations_ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 401: 'JWT Token Expires', 403: 'Unauthorized', 404: 'Not Found'})
class StationsAPI(Resource):

    @jwt_required()
    @stations_ns.doc(security="JsonWebToken")
    @stations_ns.marshal_with(stations_model)
    def get(self,id):
        '''წამოვიღოთ კონკრეტული სადგურის ინფორმაცია'''

        station = Stations.query.filter_by(id=id).first()
        if not station:
            return {"error": "სადგური არ მოიძებნა."}, 404
        
        return station, 200
    
    @jwt_required()
    @stations_ns.doc(security="JsonWebToken")
    @stations_ns.doc(parser=stations_parser)
    def put(self,id):
        '''კონკრეტული სადგურის რედაქტირება'''

        identity = get_jwt_identity()

        admin = User.query.filter_by(uuid=identity).first()
        if not admin.check_permission():
            return {"message": 'თქვენ არ გაქვთ სადგურის რედაქტირების უფლება'}, 403

        station = Stations.query.filter_by(id=id).first()
        if not station:
            return {"error": "სადგური არ მოიძებნა."}, 404
        
        args = stations_parser.parse_args()

        station.station_name = args.get('station_name')
        station.url = args.get('url')
        station.api = args.get('api')
        station.latitude = args.get('latitude')
        station.longitude = args.get('longitude')
        station.status = args.get('status')

        station.save()

        return {"message": "სადგური წარმატებით დარედაქტირდა."}, 200
    
    @jwt_required()
    @stations_ns.doc(security="JsonWebToken")
    def delete(self,id):
        '''კონკრეტული სადგურის წაშლა'''

        identity = get_jwt_identity()

        admin = User.query.filter_by(uuid=identity).first()
        if not admin.check_permission():
            return {"message": 'თქვენ არ გაქვთ სადგურის წაშლის უფლება'}, 403


        data = WeatherData.query.filter_by(station_id=id).first()
        if data:
            return {'message': 'სადგურის წაშლა წარუმატებლად დასრულდა (აღნიშნულ სადგურზე მონაცემი არსებობს)'}, 400
        else:
            station = Stations.query.filter_by(id=id).first()
            if not station:
                return {"error": "სადგური არ მოიძებნა."}, 404
            station.delete()
            return {'message': 'სადგური წარმატებით წაიშალა (აღნიშნულ სადგურზე მონაცემი არ არსებობს)'}, 200

