import logging
import sys
import os
import datetime

from src.models.weather import PrevPrecip

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src import create_app
from src.models import StationsDivPositions

LOG_FILENAME = "insert_precip_long_db.log"
logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')



def station_is_dry():
    # ეს ფუნქცია აბრუნებს 1 - ს როდესაც pa 24 საათის განმავლობაში 0 -ს უდრის, და შემდგომ ამას ვიყენებთ pa_long ის დასარესეტებლად
    global zero_start_time # es ukve raghac droa bazidan wamoghebuli (precip_time)
    elapsed_time = datetime.datetime.now() - zero_start_time
    if elapsed_time >= datetime.timedelta(hours=24):
        return 1
    else:
        return 0

def new_day_initialized(pa, prev_pa):
    if pa < prev_pa:
        return 1
    else:
        return 0


'''
unda davwerot funqcia ramdenime edge case ze:
1. rodesac shemovida --.-- ramdenjerme
2. rodesac --.-- shemovida 24 saatze metxans
3. ...
'''

def pa_long_calculator(pa):
    global pa_long, prev_pa
    if pa >= prev_pa: # monacemebi chveulebrivad shemodis (normal case)
        if station_is_dry():
            pa_long = 0   # tu 24 saatis ganmavlobashi sadgurma ar daafiqsira wvima mashin davaresetoto pa_long
            prev_pa = pa

    elif pa < prev_pa and pa > 0:
         # ამ elif-ის გააქტიურებისას იწყება ახალი დღე რადგან შემოსული pa < prev_pa, შესაბამისად ვიწყებთ pa_long += pa თვლას
        last_pa_long = pa_long + pa
        prev_pa = pa
        pa_long = last_pa_long

# როდესაც pa იქნება 0 ან --.-- მაგ შემთხვევებს მთავარ ფუნქციაში განვიხილავთ

station_dict = {}

def fetch_stations():
    global station_dict
    station_dict = {}
    try:
        stations = StationsDivPositions.query.with_entities(
            StationsDivPositions.station_id,
            StationsDivPositions.precip_accum
        ).all()
        prev_stations = PrevPrecip.query.with_entities(
            PrevPrecip.prev_pa,
            PrevPrecip.last_pa_long,
            PrevPrecip.zero_start_time
        ).all()
        if not stations:
            logging.info("No stations found.")
            return
        else:
            print(stations)

    except Exception as e:
        logging.critical(f"სკრიპტის შესრულების დროს შეცდომა: {e}")


    for station in stations:
        station_dict[station[0]] = station[1]




'''
def fill_prev_pa():
    prev_stations = PrevPrecip.query.with_entities(
        PrevPrecip.prev_pa,
        PrevPrecip.last_pa_long,
        PrevPrecip.zero_start_time
    ).all()
    
'''

def main():
    app = create_app()
    with app.app_context():
        stations = fetch_stations()


if __name__ == "__main__":
    main()