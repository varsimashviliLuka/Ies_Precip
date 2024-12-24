import requests
import logging
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src import create_app
from src.models import Stations, WeatherData
from src.config import Config

# ლოგირების კონფიგურაცია
LOG_FILENAME = "insert_precip_db.log"
logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

def fetch_stations():
    """
    მონაცემთა ბაზიდან აქტიური სადგურების ამოღება.
    """
    try:
        stations = Stations.query.with_entities(Stations.id, Stations.api).filter_by(status=1).all()
        logging.info(f"სადგურების რაოდენობა ბაზიდან: {len(stations)}")
        return stations
    except Exception as e:
        logging.error(f"ბაზიდან სადგურების მიღების შეცდომა: {e}")
        raise

def fetch_precip_data(stations):
    """
    სადგურებიდან მონაცემების მიღება API-ს საშუალებით.
    """
    precip_data = []
    for station_id, api_url in stations:
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                # მონაცემების ამოღება და ფორმატირება
                precip_rate = "{:.2f}".format(data['observations'][0]['metric']['precipRate'])
                precip_accum = "{:.2f}".format(data['observations'][0]['metric']['precipTotal'])
                precip_data.append({
                    'station_id': station_id,
                    'precip_rate': precip_rate,
                    'precip_accum': precip_accum
                })
            else:
                logging.warning(f"მონაცემების მიღება ვერ მოხერხდა სადგურისთვის {station_id}: HTTP {response.status_code}")
                precip_data.append({
                    'station_id': station_id,
                    'precip_rate': "--:--",
                    'precip_accum': "--:--"
                })
        except (requests.RequestException, KeyError, IndexError) as e:
            logging.error(f"მონაცემების მიღების ან დამუშავების შეცდომა სადგურისთვის {station_id}: {e}")
            precip_data.append({
                'station_id': station_id,
                'precip_rate': "--:--",
                'precip_accum': "--:--"
            })
    logging.info(f"მონაცემები მიღებულია {len(precip_data)} სადგურისთვის.")
    return precip_data

def insert_precip_data(precip_data):
    """
    მიღებული მონაცემების ჩაწერა მონაცემთა ბაზაში.
    """
    try:
        for data in precip_data:
            new_record = WeatherData(
                station_id=data['station_id'],
                precip_rate=data['precip_rate'],
                precip_accum=data['precip_accum']
            )
            new_record.create()
            logging.info(f"მონაცემები ჩაწერილია {len(precip_data)} სადგურისთვის.")
    except Exception as e:
        logging.error(f"მონაცემების ჩაწერის შეცდომა: {e}")
        raise


def main():
    app = create_app()
    with app.app_context():
        try:
            # სადგურების მონაცემების მიღება
            stations = fetch_stations()
            # სადგურების მონაცემებზე დაყრდნობით API-დან მონაცემების მიღება
            precip_data = fetch_precip_data(stations)
            # მონაცემების ბაზაში ჩაწერა
            insert_precip_data(precip_data)
        except Exception as e:
            logging.critical(f"სკრიპტის შესრულების დროს შეცდომა: {e}")

if __name__ == "__main__":
    main()

