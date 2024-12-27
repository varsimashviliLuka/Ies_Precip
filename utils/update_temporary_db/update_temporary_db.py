import requests
import logging
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.models import Stations, WeatherData, StationsDivPositions
from src import create_app


# ლოგებისთვის ფაილის სახელს ვანიჭებთ
LOG_FILENAME = 'update_temporary_db.log'
# ლოგების კონფიგი
logging.basicConfig(filename=LOG_FILENAME,level=logging.CRITICAL,format="%(asctime)s - %(levelname)s - %(funcName)s - %(message)s",filemode='a')

def modify_station_details(station_details):
    for station_detail in station_details:
         # http მოთხოვნას აგზავნის api-ზე რადგან წამოიღოს მონაცები
        response = requests.get(station_detail.stations.api)

        if response.status_code != 200:
             # თუ სადგურს ვერ დაუკავშირდა (გათიშუალია სადგური ან კავშირი ვერ შედგა) გაუწერს default მნიშვნელობებს და განაახლებს ბაზას
            logging.warning(f'დაკავშირება ვერ მოხერხდა {station_detail.stations.station_name} სადგურზე!')

            station_detail.first_div_height = 0.00
            station_detail.precip_rate = "--,--"
            station_detail.precip_accum = "--,--"
            station_detail.save()
            continue
    # სადგურთან კავშირის შემთხვევაში

        data = response.json()

    # მონაცემების ცვლადებში შენახვა და შემდგომ მათი ბაზაში განახლება
        try:
            precip_rate = data['observations'][0]['metric']['precipRate']
            precip_accum = data['observations'][0]['metric']['precipTotal']
            precip_rate = "{:.2f}".format(precip_rate)
            precip_accum = float("{:.2f}".format(precip_accum))
        except:
            logging.warning(f"json დან მონაცემების ამოღების დროს მოხდა შეცდომა {station_detail.stations.station_name}")
            continue


        if precip_accum == 0.0:
            top_bottom = station_detail.static_px
            first_div_height = 0.00
        else:
            top_bottom = station_detail.static_px - precip_accum
            first_div_height = precip_accum
        
        station_detail.first_div_height = first_div_height
        station_detail.top_bottom = top_bottom
        station_detail.precip_accum = precip_accum
        station_detail.precip_rate = precip_rate

        station_detail.save()

        logging.info(f'მონაცემი წარმატებით დაემატა {station_detail.stations.station_name}')


def main():
    app = create_app()
    with app.app_context():
        station_details = StationsDivPositions.query.all()
        modify_station_details(station_details)



if __name__ == '__main__':
    main()

