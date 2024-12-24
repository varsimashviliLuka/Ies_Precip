import pymysql
from dotenv import load_dotenv
import os
import datetime


load_dotenv(dotenv_path='/home/levany/PycharmProjects/Ies_Precip/.env')

MYSQL_HOST = os.getenv('MYSQL_HOST', 'default_host')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'default_database')
MYSQL_USER = os.getenv('MYSQL_USER', 'default_user')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD_TEMP', 'default_password')


def return_pa(pa):   # es funqcia gadaivlis {stations_div_positions}-s bazas da daabrunebs pa-s
####
#
#
#
#
#

    return pa






def monitor_station_is_dry(pa):
    # ეს ფუნქცია აბრუნებს 1 - ს როდესაც pa 24 საათის განმავლობაში 0 -ს უდრის, და შემდგომ ამას ვიყენებთ pa_long ის დასარესეტებლად
    zero_start_time = None
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



list_of_pa_longs = []

def pa_long_calculator(pa):
    pa = return_pa()
    prev_pa = 0
    while pa >= prev_pa:
        pa_long = pa
        prev_pa = pa


        if pa < prev_pa:
            if monitor_station_is_dry(pa):
                pa_long = 0
            else:
                while pa >= prev_pa:
                    temp_pa_long = pa_long + pa
                    if pa_long != temp_pa_long:
                        pa_long = temp_pa_long
                        # ეხა დასაწერი მაქ pa_long ის ზრდა, როდესაც 1 დღის ლუპი მორჩა და ახალი დღის მონაცემებმა დაიწყეს შემოსვლა
                        # ფორმულა უნდა იყოs - - - pa_long + pa - - -
                        # ამ დროს იწყება ახალი 24 საათი, pa რესეტდება და მისი ათვლა თავიდან იწყება
                        # ახლა მნიშვნელოვანია სწორად გავწერო კოდი რომ თუ შემოვიდა 0 ები გაჩეკოს monitor_station_if_dry ფუნქცია
                        #  თუ მან დააბრუნა 0, მაშინ გააგრძელოს pa_long ის სწორად ათვლა
                        # აქამდე ათვლილიც უნდა დაიმხასოვროს და ძველ pa_long - ს ახალი და ახალი pa ები უმატოს pa_long + pa
    if pa == 0:
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

cursor = connection.cursor()

query = "SELECT precip_accum, station_id FROM weather_data"
cursor.execute(query)
rows = cursor.fetchall()



cursor.close()
connection.close()
