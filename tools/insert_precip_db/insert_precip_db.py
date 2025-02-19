import logging
from datetime import datetime, timedelta
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src import create_app
from src.models import DivPositions, WeatherData

# from src.config import TestConfig

def fetch_precip_data():
    """
    მონაცემთა ბაზიდან აქტიური სადგურების ამოღება.
    """
    try:
        precip_data = DivPositions.query.with_entities(
            DivPositions.station_id, 
            DivPositions.precip_rate, 
            DivPositions.precip_accum, 
            DivPositions.precip_accum_long
        ).filter(DivPositions.precip_accum != "xx:xx").all()
        
        logging.debug(f"ბაზიდან ამოღებულია {len(precip_data)} ჩანაწერი.")
        return precip_data
    except Exception as e:
        logging.critical(f"ბაზიდან სადგურების მიღების შეცდომა: {e}")
        raise
    

def insert_precip_data(precip_data):
    """
    მიღებული მონაცემების ჩაწერა მონაცემთა ბაზაში.
    """
    try:
        if not precip_data:
            logging.warning("სადგურების მონაცემები ცარიელია.")
            return

        for data in precip_data:
            try:
                new_record = WeatherData(
                    station_id=data.station_id,  # დარწმუნდით, რომ ველები ემთხვევა
                    precip_rate=data.precip_rate,
                    precip_accum=data.precip_accum,
                    precip_accum_long=data.precip_accum_long,
                    precip_time=datetime.now() + timedelta(hours=4)
                )
                new_record.create()
                logging.debug(f"მონაცემები ჩაწერილია სადგურისთვის: {data.station_id}")
            except Exception as e:
                logging.error(f"ჩაწერის შეცდომა სადგურისთვის {data.station_id}: {e}")
    except Exception as e:
        logging.critical(f"მონაცემების ჩაწერის პროცესში კრიტიკული შეცდომა: {e}")
        raise

def insert_precip_db():
    """
    მთავარი ფუნქცია, რომელიც მონაცემებს იბარებს და ჩაწერს ბაზაში.
    """
    app = create_app()
    # app = create_app(TestConfig)
    with app.app_context():
        try:
            precip_data = fetch_precip_data()
            insert_precip_data(precip_data)
        except Exception as e:
            logging.critical(f"სკრიპტის შესრულების დროს კრიტიკული შეცდომა: {e}")

if __name__ == "__main__":
    insert_precip_db()