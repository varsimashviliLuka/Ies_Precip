from flask_restx import Resource
from flask_jwt_extended import jwt_required
import requests
import time
from src.api.nsmodels import stations_div_positions_ns, stations_div_positions_model
from src.models import StationsDivPositions

# Cache to store the last API response and timestamp
api_cache = {}
CACHE_TIMEOUT = 40  # Timeout in seconds

@stations_div_positions_ns.route('/stations/div_positions')
@stations_div_positions_ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 401: 'JWT Token Expired', 403: 'Unauthorized', 404: 'Not Found'})
class StationsDivPositionsApi(Resource):

    @stations_div_positions_ns.marshal_with(stations_div_positions_model)
    @jwt_required()
    @stations_div_positions_ns.doc(security="JsonWebToken")
    def get(self):
        '''Fetch all station div information'''


        stations_div_positions = StationsDivPositions.query.all()
        if not stations_div_positions:
            return {"error": "სადგურები არ მოიძებნა."}, 404

        result = []

        for i in stations_div_positions:

            api_link = i.stations.api
            current_time = time.time()

            # Check if the API link is in the cache and if the timeout has not expired
            if api_link in api_cache:
                cached_data = api_cache[api_link]
                if current_time - cached_data['timestamp'] < CACHE_TIMEOUT:
                    result.append(cached_data['data'])
                    continue

            first_div_height = 0.00
            PRECIP_ACCUM = "--,--"
            PRECIP_RATE = "--,--"

            final = {
                'PRECIP_ACCUM': PRECIP_ACCUM,
                'PRECIP_RATE': PRECIP_RATE,
                'Station': i.stations.station_name,
                'Url': i.stations.url,
                'api': i.stations.api,
                'first_div_height': first_div_height,

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

            try:
                response = requests.get(api_link)
                if response.status_code != 200:
                    result.append(final)
                    continue

                data = response.json()

                try:
                    PRECIP_RATE = data['observations'][0]['metric']['precipRate']
                    PRECIP_ACCUM = data['observations'][0]['metric']['precipTotal']
                    PRECIP_RATE = "{:.2f}".format(PRECIP_RATE)
                    PRECIP_ACCUM = "{:.2f}".format(PRECIP_ACCUM)
                    PRECIP_ACCUM = float(PRECIP_ACCUM)
                except:
                    print("Error extracting data from JSON")
                    result.append(final)
                    continue

                if PRECIP_ACCUM == 0.0:
                    top_bottom = i.static_px
                    first_div_height = 0.00
                else:
                    top_bottom = i.static_px - PRECIP_ACCUM
                    first_div_height = PRECIP_ACCUM

                final['top_bottom'] = top_bottom
                final['first_div_height'] = first_div_height
                final['PRECIP_ACCUM'] = PRECIP_ACCUM
                final['PRECIP_RATE'] = PRECIP_RATE

                # Update cache
                api_cache[api_link] = {
                    'data': final,
                    'timestamp': current_time
                }

            except requests.RequestException as e:
                print(f"Request error: {e}")

            result.append(final)

        return result, 200
