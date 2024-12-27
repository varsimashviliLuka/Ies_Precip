from os import WCONTINUED

import pymysql
from dotenv import load_dotenv
import os
import datetime

load_dotenv(dotenv_path='/home/levany/PycharmProjects/Ies_Precip/.env')

MYSQL_HOST = os.getenv('MYSQL_HOST', 'default_host')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'default_database')
MYSQL_USER = os.getenv('MYSQL_USER', 'default_user')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD_TEMP', 'default_password')

def monitor_station_is_dry():
    # ეს ფუნქცია აბრუნებს 1 - ს როდესაც pa 24 საათის განმავლობაში 0 -ს უდრის, და შემდგომ ამას ვიყენებთ pa_long ის დასარესეტებლად
    global zero_start_time # es ukve raghac droa bazidan wamoghebuli
    elapsed_time = datetime.datetime.now() - zero_start_time
    if elapsed_time >= datetime.timedelta(hours=24):
        pa_long = 0
    return pa_long

def new_day_initialized(pa, prev_pa):
    if pa < prev_pa:
        return 1
    else:
        return 0




def pa_long_calculator(pa):
    global pa_long, prev_pa
    if new_day_initialized(pa,prev_pa) == 0 and pa >= prev_pa: # axali dghe ar dawyebula...
        if monitor_station_is_dry()
        pa_long = pa
        prev_pa = pa
    elif pa < prev_pa and pa > 0:
         # ამ else-ის გააქტიურებისას იწყება ახალი დღე რადგან შემოსული pa < prev_pa, შესაბამისად ვიწყებთ pa_long += pa თვლას
        temp_pa_long = pa_long + pa
        prev_pa = pa
        if pa_long < temp_pa_long:
            pa_long = temp_pa_long
    else: # როცა pa არი 0
        if monitor_station_is_dry(pa):
            pa_long = 0
    return (pa_long)

'''
import pymysql
from dotenv import load_dotenv
import os
import datetime


load_dotenv(dotenv_path='/home/levany/PycharmProjects/Ies_Precip/.env')

MYSQL_HOST = os.getenv('MYSQL_HOST', 'default_host')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'default_database')
MYSQL_USER = os.getenv('MYSQL_USER', 'default_user')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD_TEMP', 'default_password')

prev_pa = 0
pa_long = 0
zero_start_time = None

def return_pa(pa):   # es funqcia gadaivlis {stations_div_positions}-s bazas da daabrunebs pa-s

    return pa
tempo = 3




def monitor_station_is_dry(pa):
    # ეს ფუნქცია აბრუნებს 1 - ს როდესაც pa 24 საათის განმავლობაში 0 -ს უდრის, და შემდგომ ამას ვიყენებთ pa_long ის დასარესეტებლად
    global zero_start_time
    if pa == 0:
        if zero_start_time is None:
            zero_start_time = datetime.datetime.now()  # იწყება 24 საათიანი ტაიმერი
        else:
            elapsed_time = datetime.datetime.now() - zero_start_time
            if elapsed_time >= datetime.timedelta(hours=24):
                return 1  # როდესაც 24 საათი გავა დავაბრუნოთ 1
    else:
        zero_start_time = None  # დავარესეტოთ ტაიმერი როდესაც pa > 0
    return False


def pa_long_calculator(pa):
    pa = return_pa(tempo)
    global pa_long, prev_pa
    if pa >= prev_pa: #pa_long = 4.06, prev_pa = 4.06, pa = 0
        pa_long = pa
        prev_pa = pa
    elif pa < prev_pa and pa > 0:
         # ამ else-ის გააქტიურებისას იწყება ახალი დღე რადგან შემოსული pa < prev_pa, შესაბამისად ვიწყებთ pa_long += pa თვლას
        temp_pa_long = pa_long + pa
        prev_pa = pa
        if pa_long < temp_pa_long:
            pa_long = temp_pa_long
    else: # როცა pa არი 0
        if monitor_station_is_dry(pa):
            pa_long = 0
    return (pa_long)



try:
    connection = pymysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )
except Exception as err:
    print(f"ბაზასთან კავშირი ვერ შედგა - {err}")
    exit()

cursor = connection.cursor()

query = "SELECT precip_accum, station_id FROM weather_data"
cursor.execute(query)
rows = cursor.fetchall()

for row in rows:
    pa = row[0]


cursor.close()
connection.close()

'''