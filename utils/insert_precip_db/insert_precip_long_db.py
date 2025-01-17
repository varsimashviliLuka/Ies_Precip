import logging
import sys
import os
import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src import create_app
from src.models import DivPositions, PrevPrecip

LOG_FILENAME = "insert_precip_long_db.log"
logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')


def fetch_pa(): # შემდეგ ფუნქციას მონაცემები მოაქვს prev_precip & div_positions მონაცემთა ბაზებიდან

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

# ეს ფუნქცია ითვლის pa_long-ს  ქვემოთ ჩამოთვლილი მონაცემების გამოყენებით
def calc_pa_long(stations_pa, prev_stations):
    for station, prev_station in zip(stations_pa, prev_stations):
        pa = station.precip_accum
        pa_long = station.precip_accum_long
        prev_pa = prev_station.prev_pa
        zero_start_time = prev_station.zero_start_time
        last_pa_long = prev_station.last_pa_long

        # ეს არის ალგორითმი რომელიც ითვლის pa_long ს.
        if pa != '--:--':
            pa = float(pa)

        if (pa == 0 or pa == '--:--') and prev_pa !=0:
            zero_start_time = datetime.datetime.now()
            prev_pa = 0.0

        elif (pa == 0 or pa == '--:--') and prev_pa == 0:
            elapsed_time = datetime.datetime.now() - zero_start_time
            prev_pa = 0.0
            if elapsed_time >= datetime.timedelta(hours=24):
                pa_long = 0
                zero_start_time = datetime.datetime.now()

        elif pa >= prev_pa:
            pa_long = pa + last_pa_long
            prev_pa = pa

        elif 0 < pa < prev_pa:
            last_pa_long = pa_long
            pa_long = last_pa_long + pa
            prev_pa = pa

        if station:
            station.precip_accum_long = pa_long
            station.save()
        if prev_station:
            prev_station.prev_pa = prev_pa
            prev_station.zero_start_time = zero_start_time
            prev_station.last_pa_long = last_pa_long
            prev_station.save()

def main():
    app = create_app()
    with app.app_context():
        stations_pa, prev_stations = fetch_pa()
        if stations_pa is None or prev_stations is None:
            logging.error("Failed to fetch data. Exiting.")
            return

        # Perform calculations
        calc_pa_long(stations_pa, prev_stations)

if __name__ == "__main__":
    main()