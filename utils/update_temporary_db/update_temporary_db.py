import pymysql
import os
from dotenv import load_dotenv
import requests
import logging

# დირექტორიას ვცვლით, რადგან შევძლოთ .env-ში არსებული კონფიგების გამოყენება
load_dotenv(dotenv_path='../../.env')

# ლოგებისთვის ფაილის სახელს ვანიჭებთ
self_name = 'update_temporary_db.log'

# ლოგების კონფიგი
logging.basicConfig(filename=self_name,level=logging.INFO,format="%(asctime)s - %(levelname)s - %(funcName)s - %(message)s",filemode='a')

# mysql ბაზასთან კავშირი
MYSQL_HOST = os.getenv('MYSQL_HOST', 'default_host')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'default_database')
MYSQL_USER = os.getenv('MYSQL_USER', 'default_user')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD_TEMP', 'default_password')

# მოწმდება რამდენად შედგა კავშირი ბაზასთან
try:
    connection = pymysql.connect(
    host=MYSQL_HOST,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DATABASE
)
except Exception as e:
# თუ ვერ დაუკავშირდა აბრუნებს კრიტიკალის ლოგს და თიშავს პროგრამას
    logging.critical(f'ბაზასთან კავშირი ვერ შედგა. error: {e}')
    exit()

# იქმნება კურსორი
cursor = connection.cursor()

def main():
    # მოაქვს მონაცემები stations_div_positions table-დან
    query = "SELECT * FROM stations_div_positions"
    cursor.execute(query)

    data = cursor.fetchall()

    if not data:
        logging.error('ბაზაში div მონაცემი ვერ მოიძებნა')
    
    for i in data:

        # უცვლელი მონაცემი
        data_id = i[0]
        station_id = i[1]
        static_px = i[2]

        # ცვალებადი მონაცემი
        first_div_height = i[9]
        precip_accum = i[10]
        precip_rate = i[11]
        top_bottom = i[12]
        # მოაქვს სადგური stations table-დან კონკრეტული station_id ით 
        query = f"SELECT * FROM stations WHERE id={station_id}"
        cursor.execute(query)

        station = cursor.fetchone()

        if not station:
            logging.warning(f'{station_id} id-ით სადგური ვერ მოიძებნა')

        # http მოთხოვნას აგზავნის api-ზე რადგან წამოიღოს მონაცები
        api_link = station[3]
        response = requests.get(api_link)

        if response.status_code != 200:

            logging.warning(f'დაკავშირება ვერ მოხერხდა {station[1]} სადგურზე!')

            # თუ სადგურს ვერ დაუკავშირდა (გათიშუალია სადგური ან კავშირი ვერ შედგა) გაუწერს default მნიშვნელობებს და განაახლებს ბაზას
            
            first_div_height = 0.00
            precip_rate = "--,--"
            precip_accum = "--,--"
            query = f'UPDATE stations_div_positions SET first_div_height={first_div_height}, top_bottom={top_bottom}, precip_accum="{precip_accum}", precip_rate="{precip_rate}" WHERE id={data_id}'
            cursor.execute(query)
            connection.commit()
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
            logging.warning(f"json დან მონაცემების ამოღების დროს მოხდა შეცდომა {station[1]}")
            continue

        if precip_accum == 0.0:
            top_bottom = static_px
            first_div_height = 0.00
        else:
            top_bottom = static_px - precip_accum
            first_div_height = precip_accum

        query = f'UPDATE stations_div_positions SET first_div_height={first_div_height}, top_bottom={top_bottom}, precip_accum={precip_accum}, precip_rate={precip_rate} WHERE id={data_id}'
        cursor.execute(query)
        connection.commit()
        logging.info(f'მონაცემი წარმატებით დაემატა {station[1]}')

# კავშირის შეწყვეტა ბაზასთან

    cursor.close()
    connection.close()

if __name__ == '__main__':
    main()

