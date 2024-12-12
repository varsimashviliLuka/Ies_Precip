import pytest
import requests



token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTczNDAwMzEzMCwianRpIjoiNmZkZWIyYmQtNjI0NS00YjBlLTk0ZDUtNDQxODIwY2VhMGFjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjVjMzc2YjRhLWE5MDQtNDFlMC1iOTNlLTA1Y2E2NGY1ZmQxMCIsIm5iZiI6MTczNDAwMzEzMCwiY3NyZiI6ImRjMzc2MjY4LWU5ZGItNDlhMi04YTUzLWYzY2E4NGQ4MzI3OCIsImV4cCI6MTczNDAwNjczMH0.f9Osk1uVc_6i2GEp1Wt2lLgVYbnaoNenAcndrCfgB4w"



    # Add the Bearer token to the headers
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"  # Optional: Specify if your request body is JSON
}


example = {
                    "id": 1,
                    "station_name": "Bazaleti - IUNDILAA2",
                    "url": "https://www.wunderground.com/dashboard/pws/IUNDILAA2",
                    "api": "https://api.weather.com/v2/pws/observations/current?apiKey=e1f10a1e78da46f5b10a1e78da96f525&stationId=IUNDILAA2&numericPrecision=decimal&format=json&units=m",
                    "latitude": 42.06,
                    "longitude": 44.67,
                    "status": True
                    }


class TestStations:
    def test_get_stations(self):
        url = "http://localhost:5000/api/stations"
        
        r = requests.get(url,headers=headers).json()[0]

        print(type(r['longitude']))

        if set(example.keys()) == set(r.keys()):
            assert True
        else:
            assert False


    def test_get_station(self):
        url = "http://localhost:5000/api/stations/6"

        
        r = requests.get(url,headers=headers).json()

        if set(example.keys()) == set(r.keys()):
            assert True
        else:
            assert False