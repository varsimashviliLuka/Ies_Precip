# CREATE TABLE stations (id INT AUTO_INCREMENT PRIMARY KEY, station_name VARCHAR(256),url VARCHAR(512),api VARCHAR(512),latitude DECIMAL(9, 6),longitude DECIMAL(9, 6));
# CREATE TABLE weather_data (id INT AUTO_INCREMENT PRIMARY KEY, station_id INT,precip_rate VARCHAR(128),precip_accum VARCHAR(128),precip_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,FOREIGN KEY (station_id) REFERENCES stations(id));
# insert into stations (station_name, url, api,latitude, longitude) values ("Bazaleti - IUNDILAA2", "https://www.wunderground.com/dashboard/pws/IUNDILAA2", "https://api.weather.com/v2/pws/observations/current?apiKey=e1f10a1e78da46f5b10a1e78da96f525&stationId=IUNDILAA2&numericPrecision=decimal&format=json&units=m", 42.06, 44.67);
# insert into weather_data (station_id, precip_rate, precip_accum) values (1, "20.64", "10.23");
# select stations.station_name, stations.url, stations.latitude, stations.longitude, weather_data.precip_rate, weather_data.precip_accum, weather_data.precip_time  from stations  left join weather_data on stations.id = weather_data.station_id;

import mysql.connector

from logs import print_and_log

try:
    mydb = mysql.connector.connect(
        host        ="localhost",
        user        ="root",
        password    ="Ml@Root88",
        database    ="weather"
    )
except Exception as err:
    print_and_log("ბაზასთან დაკავშირებისას მოხდა შეცდომა",err )


def get_stations():
    mycursor = mydb.cursor()
    mycursor.execute("select id, api from stations where status = 1;")
    result = mycursor.fetchall()
    return result





def insert_data(weather_data):
    mycursor = mydb.cursor()
    for data in weather_data:
        mycursor.execute(f'insert into weather_data (station_id, precip_rate, precip_accum) values ({data[0]}, "{data[1]}", "{data[2]}");')
        mydb.commit()
    
    mydb.close()




