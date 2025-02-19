from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.api.nsmodels import stations_ns, stations_model, stations_parser
from src.models import Stations, WeatherData, User, DivPositions, PrevPrecip

from datetime import datetime

import requests




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

        # მოწმდება რამდენად აქვთ მომხმარებელს სადგურის დამატების უფლება

        admin = User.query.filter_by(uuid=identity).first()
        if not admin.check_permission():
            return {"error": 'თქვენ არ გაქვთ სადგურის დამატების უფლება'}, 403

        args = stations_parser.parse_args()

        # მითითებული ლინკი იყოფა ნაწილებად, სადაც ბოლო ნაწილი ყოველთვის რჩება სადგურის ID რისი საშუალებითაც იქმნება API ლინკი

        shorten_station_name = args.get('url').split('/')[-1]
        api_url = f'https://api.weather.com/v2/pws/observations/current?apiKey=e1f10a1e78da46f5b10a1e78da96f525&stationId={shorten_station_name}&numericPrecision=decimal&format=json&units=m'

        url = args.get('url')


        # მოწმდება რამდენად შესაძლებელია სადგურის დამატება

        station = Stations.query.filter_by(url=url).first()
        if station:
            return {'error': 'აღნიშნული სადგური უკვე არსებობს'}, 400

        # API-ის ლინკთან კავშირის დამყარება, რომ გავიგოთ სადგური არსებობს თუ არა

        response = requests.get(api_url)

        if response.status_code != 200:
            return {'error': 'გთხოვთ შეიყვანეთ სწორი ლინკი'}, 400
        
        # იქმნება სადგური მომხმარებლის მიერ შეყვანილი პარამეტრებით

        new_station = Stations(station_name = args.get('station_name'),
                               url = url,
                               api = api_url,
                               latitude = args.get('latitude'),
                               longitude = args.get('longitude'),
                               status=args.get('status'))

        new_station.create()

        # ასევე ემატება პოზიციების ცხრილში, default მონაცემებით

        new_div_position = DivPositions(station_id=new_station.id,
                                        static_px=-20,
                                        left_right=20,
                                        line_rotate=0,
                                        line_left_right=0,
                                        line_top_bottom=0,
                                        shorten_station_name=shorten_station_name,
                                        map_status=args.get('map_status'),
                                        first_div_height=0,
                                        precip_accum=0,
                                        precip_rate=0,
                                        precip_accum_long=0,
                                        top_bottom=-45)
        new_div_position.create()

        # ემატება precip ცხრილშიც, რადგან მოხდეს მისი pa_long ის დათვლა

        new_prev_precip = PrevPrecip(station_id=new_station.id,
                                     prev_pa=0,
                                     last_pa_long=0,
                                     zero_start_time=datetime.now())
        
        new_prev_precip.create()

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

        # მოწმდება მომხმარებლის უფლებები, თუ აქვს მას სადგურის რედაქტირების უფლება

        identity = get_jwt_identity()

        admin = User.query.filter_by(uuid=identity).first()
        if not admin.check_permission():
            return {"error": 'თქვენ არ გაქვთ სადგურის რედაქტირების უფლება'}, 403

        # ვეძებთ მითითებული ID-ით სადგურს

        station = Stations.query.filter_by(id=id).first()
        if not station:
            return {"error": "სადგური არ მოიძებნა."}, 404
        
        div_position = DivPositions.query.filter_by(station_id=id).first()
        if not div_position:
            return {"error": "სადგური არ მოიძებნა."}, 404
        
        args = stations_parser.parse_args()

        # ვეძებთ სადგურს, რომელსაც გააჩნია მომხმარებლის მიერ შეყვანილი url ლინკი და არ არის თვითონ კონკრეტულად ეს სადგური

        checker_station = Stations.query.filter(Stations.url == args.get('url'), Stations.id != id).first()

        # თუ არსებობს ასეთი სადგური, გავდივართ ერორზე, რომ არ მოხდეს სადგურების და ინფორმაციის დუპლიკაცია

        if checker_station:
            return {'error': 'აღნიშნული სადგური უკვე არსებობს!'}, 400

        # იქმნება ახალი API ლინკი ახალ url-ზე მორგებული 

        shorten_station_name = args.get('url').split('/')[-1]
        api_url = f'https://api.weather.com/v2/pws/observations/current?apiKey=e1f10a1e78da46f5b10a1e78da96f525&stationId={shorten_station_name}&numericPrecision=decimal&format=json&units=m'

        # მონაცემები ნახლდება

        station.station_name = args.get('station_name')
        station.url = args.get('url')
        station.api = api_url
        station.latitude = args.get('latitude')
        station.longitude = args.get('longitude')
        station.status = args.get('status')

        div_position.map_status=args.get('map_status')

        div_position.save()
        station.save()

        return {"message": "სადგური წარმატებით დარედაქტირდა."}, 200
    
    @jwt_required()
    @stations_ns.doc(security="JsonWebToken")
    def delete(self,id):
        '''კონკრეტული სადგურის წაშლა'''

        # მოწმდება აქვს თუ არა მომხმარებელს სადგურის წაშლის უფლება

        identity = get_jwt_identity()

        admin = User.query.filter_by(uuid=identity).first()
        if not admin.check_permission():
            return {"error": 'თქვენ არ გაქვთ სადგურის წაშლის უფლება'}, 403


        data = WeatherData.query.filter_by(station_id=id).first()
        if data:
            return {'error': 'სადგურის წაშლა წარუმატებლად დასრულდა (აღნიშნულ სადგურზე მონაცემი არსებობს)'}, 400
        else:
            station = Stations.query.filter_by(id=id).first()
            if not station:
                return {"error": "სადგური არ მოიძებნა."}, 404
            station.delete()
            return {'message': 'სადგური წარმატებით წაიშალა (აღნიშნულ სადგურზე მონაცემი არ არსებობს)'}, 200

