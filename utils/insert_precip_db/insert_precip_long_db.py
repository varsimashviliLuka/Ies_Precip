import logging
import sys
import os
import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src import create_app
from src.models import DivPositions, PrevPrecip

LOG_FILENAME = "insert_precip_long_db.log"
logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')


def fetch_pa():
    global pa,prev_pa,zero_start_time,last_pa_long
    try:
        stations_pa = DivPositions.query.all()
        prev_stations = PrevPrecip.query.all()
        if not stations_pa or not prev_stations:
            logging.info("No stations found.")
            return None, None
        else:
            return stations_pa, prev_stations

    except Exception as e:
        logging.critical(f"სკრიპტის შესრულების დროს შეცდომა: {e}")
        return None, None



def calc_pa_long(stations_pa, prev_stations):
    for prev_station in prev_stations:
        prev_station.prev_pa = 5.0

        prev_station.save()





'''
if pa >= prev_pa:  # monacemebi chveulebrivad shemodis (normal case)
     pa_long = pa + last_pa_long

elif pa < prev_pa and pa > 0:
     # ამ elif-ის გააქტიურებისას იწყება ახალი დღე რადგან შემოსული pa < prev_pa, შესაბამისად ვიწყებთ pa_long += pa თვლას
     last_pa_long = pa_long
     pa_long = last_pa_long + pa
elif pa == 0 or pa == '--:--':

     elapsed_time = datetime.datetime.now() - zero_start_time

     if elapsed_time >= datetime.timedelta(hours=24):
         pass

'''


    #       5


def main():
    app = create_app()
    with app.app_context():
        stations_pa, prev_stations = fetch_pa()
        if stations_pa is None or prev_stations is None:
            logging.error("Failed to fetch data. Exiting.")
            return
        print(stations_pa)
        # Perform calculations
        calc_pa_long(stations_pa, prev_stations)

if __name__ == "__main__":
    main()