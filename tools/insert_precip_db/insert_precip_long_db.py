import logging
import sys
import os
import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src import create_app
from src.models import DivPositions, PrevPrecip

# from src.config import TestConfig

# ეს ფუნქცია ითვლის pa_long-ს  ქვემოთ ჩამოთვლილი მონაცემების გამოყენებით
def calc_pa_long(stations_pa, prev_precips):
    for station, prev_precip in zip(stations_pa, prev_precips):
        pa = station.precip_accum
        pa_long = station.precip_accum_long
        prev_pa = prev_precip.prev_pa
        zero_start_time = prev_precip.zero_start_time
        last_pa_long = prev_precip.last_pa_long

        # ეს არის ალგორითმი რომელიც ითვლის pa_long ს.
        if pa != '--:--' and pa != 'xx:xx':
            pa = float(pa)

        if (pa == 0.0 or pa == '--:--' or pa == 'xx:xx') and (prev_pa !=0.0):
            zero_start_time = datetime.datetime.now()
            prev_pa = 0.0
            last_pa_long = pa_long

        elif (pa == 0.0 or pa == '--:--' or pa == 'xx:xx') and (prev_pa == 0.0):
            elapsed_time = datetime.datetime.now() - zero_start_time

            if elapsed_time >= datetime.timedelta(hours=24):
                pa_long = 0.0
                last_pa_long = 0.0
                zero_start_time = datetime.datetime.now()

        elif pa >= prev_pa:
            pa_long = pa + last_pa_long
            prev_pa = pa

        elif 0.0 < pa < prev_pa:
            last_pa_long = pa_long
            prev_pa = pa

        if station:
            # print("AKKKK!!!!!",pa_long)
            station.precip_accum_long = f'{float(pa_long):.2f}'
            station.save()
        if prev_precip:
            prev_precip.prev_pa = prev_pa
            prev_precip.zero_start_time = zero_start_time
            prev_precip.last_pa_long = last_pa_long
            prev_precip.save()

def insert_precip_long_db():
    app = create_app()
    # app = create_app(TestConfig)
    with app.app_context():
        try:
            stations_pa = DivPositions.query.all()
            prev_precips = PrevPrecip.query.all()
            calc_pa_long(stations_pa, prev_precips)
            logging.debug(f'pa_long-ის მონაცემი წარმატებით დაემატა.')

        except Exception as e:
            logging.critical(f"სკრიპტის შესრულების დროს შეცდომა: {e}")
        
if __name__ == "__main__":
    insert_precip_long_db()