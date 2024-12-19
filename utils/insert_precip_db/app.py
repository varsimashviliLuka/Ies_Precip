import requests

from insert_db import get_stations
from insert_db import insert_data
from logs import print_and_log


weather_data = []

def get_data(result):
    for i in result:
            response = requests.get(i[1])

            if response.status_code == 200:
                data = response.json()
                try:
                    PRECIP_RATE = data['observations'][0]['metric']['precipRate']
                    PRECIP_ACCUM = data['observations'][0]['metric']['precipTotal']
                    PRECIP_RATE = "{:.2f}".format(PRECIP_RATE)
                    PRECIP_ACCUM = "{:.2f}".format(PRECIP_ACCUM)
                except:                                    
                    data = [i[0],"--:--","--:--"]
                    weather_data.append(data)
                    print("json დან მონაცემების ამოღების დროს მოხდა შეცდომა")
                    continue
                
                data = [i[0],PRECIP_RATE,PRECIP_ACCUM]
                weather_data.append(data)
            else:      
                data = [i[0],"--:--","--:--"]
                weather_data.append(data)


try:
    result = get_stations()
    get_data(result)
    insert_data(weather_data)
except Exception as err:
     print_and_log("ფუნქციის გამოძახების დროს მოხდა შეცდომა", err)





