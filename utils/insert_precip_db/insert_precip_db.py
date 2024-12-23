import requests
import pymysql
import os
from dotenv import load_dotenv
import logging

# გარემოს ცვლადების ჩატვირთვა
load_dotenv('../../.env')

# ლოგირების კონფიგურაცია
LOG_FILENAME = "export_csv_from_db.log"
logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

# მონაცემთა ბაზის პარამეტრები
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD_STR')

# ვამოწმებთ, რომ ყველა საჭირო პარამეტრი არსებობს
if not all([MYSQL_HOST, MYSQL_DATABASE, MYSQL_USER, MYSQL_PASSWORD]):
    raise ValueError("მონაცემთა ბაზის პარამეტრები დაკარგულია!")

def connect_db():
    """
    მონაცემთა ბაზასთან კავშირის შექმნა.
    """
    try:
        connection = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )
        logging.info("მონაცემთა ბაზასთან კავშირი წარმატებით შესრულდა.")
        return connection
    except pymysql.MySQLError as e:
        logging.error(f"მონაცემთა ბაზასთან კავშირი ვერ მოხერხდა: {e}")
        raise

def fetch_stations(connection):
    """
    მონაცემთა ბაზიდან აქტიური სადგურების ამოღება.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, api FROM stations WHERE status = 1;")
            stations = cursor.fetchall()
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
                precip_data.append((station_id, precip_rate, precip_accum))
            else:
                logging.warning(f"მონაცემების მიღება ვერ მოხერხდა სადგურისთვის {station_id}: HTTP {response.status_code}")
                precip_data.append((station_id, "--:--", "--:--"))
        except (requests.RequestException, KeyError, IndexError) as e:
            logging.error(f"მონაცემების მიღების ან დამუშავების შეცდომა სადგურისთვის {station_id}: {e}")
            precip_data.append((station_id, "--:--", "--:--"))
    logging.info(f"მონაცემები მიღებულია {len(precip_data)} სადგურისთვის.")
    return precip_data

def insert_precip_data(connection, precip_data):
    """
    მიღებული მონაცემების ჩაწერა მონაცემთა ბაზაში.
    """
    try:
        with connection.cursor() as cursor:
            for station_id, precip_rate, precip_accum in precip_data:
                cursor.execute("""
                    INSERT INTO weather_data (station_id, precip_rate, precip_accum)
                    VALUES (%s, %s, %s);
                """, (station_id, precip_rate, precip_accum))
            connection.commit()
            logging.info(f"მონაცემები ჩაწერილია {len(precip_data)} სადგურისთვის.")
    except Exception as e:
        logging.error(f"მონაცემების ჩაწერის შეცდომა: {e}")
        connection.rollback()
        raise

if __name__ == "__main__":
    try:
        # მონაცემთა ბაზასთან კავშირის დამყარება
        connection = connect_db()
        # სადგურების მონაცემების მიღება
        stations = fetch_stations(connection)
        # სადგურების მონაცემებზე დაყრდნობით API-დან მონაცემების მიღება
        precip_data = fetch_precip_data(stations)
        # მონაცემების ბაზაში ჩაწერა
        insert_precip_data(connection, precip_data)
    except Exception as e:
        logging.critical(f"სკრიპტის შესრულების დროს შეცდომა: {e}")
    finally:
        # მონაცემთა ბაზასთან კავშირის დახურვა
        if connection:
            connection.close()
            logging.info("მონაცემთა ბაზასთან კავშირი დახურულია.")
