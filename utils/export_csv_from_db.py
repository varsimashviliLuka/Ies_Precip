import pymysql
import csv
import os
from dotenv import load_dotenv
import logging

# გარემოს ცვლადების ჩატვირთვა
load_dotenv('../../.env')

# logging-ის კონფიგურაცია
log_filename = "export_csv_from_db.log"
logging.basicConfig(filename=log_filename , level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

# მონაცემთა ბაზის პარამეტრები
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD_CSV')

# გარემოს ცვლადების შემოწმება
if not all([MYSQL_HOST, MYSQL_DATABASE, MYSQL_USER, MYSQL_PASSWORD]):
    raise ValueError("მონაცემთა ბაზის პარამეტრები დაკარგულია!")

# შემომავალი თარიღები
START_DATE = '2024-06-26'
END_DATE = '2024-06-28'
OUTPUT_FILE = f'../weather_data_{START_DATE}_{END_DATE}.csv'

# SQL მოთხოვნა
SQL_QUERY = f"SELECT * FROM weather_data WHERE precip_time > '{START_DATE}' AND precip_time < '{END_DATE}'"

def connection_db():
    # მონაცემთა ბაზასთან კავშირის ტესტი
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
        raise  # შეცდომის გადაცემა, რომ პროგრამა შეწყდეს

def export_csv_from_db(connection):
    # მოთხოვნის შესრულება და CSV-ში ექსპორტი
    try:
        with connection.cursor() as cursor:
            # მოთხოვნის შესრულება
            cursor.execute(SQL_QUERY)
            rows = cursor.fetchall()
            headers = [col[0] for col in cursor.description]  # სვეტების სახელები

        # მონაცემების ჩაწერა CSV ფაილში
        with open(OUTPUT_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(headers)  # სათაურების ჩაწერა
            writer.writerows(rows)   # მონაცემების ჩაწერა

        logging.info(f"მონაცემები წარმატებით ექსპორტირდა ფაილში: {OUTPUT_FILE}")
    except Exception as e:
        logging.error(f"მოთხოვნის ან ექსპორტის პროცესში შეცდომა მოხდა: {e}")
    finally:
        # კავშირის დახურვა
        connection.close()
        logging.info("მონაცემთა ბაზასთან კავშირი დახურულია.")

if __name__ == "__main__":
    try:
        connection = connection_db()  # მონაცემთა ბაზის კავშირი
        export_csv_from_db(connection)  # CSV ექსპორტი
    except Exception as e:
        logging.error(f"პროგრამის შესრულებისას მოხდა შეცდომა: {e}")
