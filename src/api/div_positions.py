from flask_restx import Resource
from src.api.nsmodels import div_positions_ns, div_positions_model
from src.models import DivPositions

@div_positions_ns.route('/stations/div_positions')
@div_positions_ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 401: 'JWT Token Expired', 403: 'Unauthorized', 404: 'Not Found'})
class DivPositionsApi(Resource):

    @div_positions_ns.marshal_with(div_positions_model)
    def get(self):
        '''Fetch all station's current div information'''

        stations_div_positions = DivPositions.query.all()
        
        if not stations_div_positions:
            return {"error": "სადგურები არ მოიძებნა."}, 404

        result = []

        for i in stations_div_positions:

            data = {
                'PRECIP_ACCUM': i.precip_accum,
                'PRECIP_RATE': i.precip_rate,
                'Station': i.stations.station_name,
                'Url': i.stations.url,
                'api': i.stations.api,
                'first_div_height': i.first_div_height,

                'id': i.shorten_station_name,

                'latitude': i.stations.latitude,
                'left_right': i.left_right,
                'line_left_right': i.line_left_right,
                'line_rotate': i.line_rotate,
                'line_top_bottom': i.line_top_bottom,
                'longitude': i.stations.longitude,
                'static_px': i.static_px,
                'map_status': i.map_status,
                'top_bottom': i.top_bottom
            }
            result.append(data)

        return result, 200
