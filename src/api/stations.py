from flask_restx import Resource

from src.api.nsmodels import stations_ns, stations_model
from src.models import Stations


@stations_ns.route('/stations')
@stations_ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 401: 'JWT Token Expires', 403: 'Unauthorized', 404: 'Not Found'})
class StationAPI(Resource):

    @stations_ns.marshal_with(stations_model)
    def get(self):
        stations = Stations.query.all()
        if not stations:
            return {"error": "სადგურები არ მოიძებნა."}, 404
        
        return stations, 200