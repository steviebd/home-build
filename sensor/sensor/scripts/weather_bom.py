import requests
import json
from time import sleep
from dbwriter import writeinflux

measurement_name = "BOM Weather"

# Measurements from the BOM URL to pull and input.
data_points_to_collect = ('gust_kmh', 
    'air_temp', 
    'dewpt', 
    'press', 
    'rel_hum', 
    'wind_spd_kmh'
)
# Datafeed from http://www.bom.gov.au/catalogue/data-feeds.shtml under Observations - individual stations for .json files
BOMURL = 'http://reg.bom.gov.au/fwo/IDN60901/IDN60901.94765.json'

def pulldatafrombom():
    try:
        r = requests.get(BOMURL)
    except requests.exceptions.Timeout:
        print('requests.exceptions.Timeout')
        sleep(7200)
        r = requests.get(BOMURL)
    except requests.exceptions.ConnectionError:
        sleep(7200)
        print('Connection to the website or database is down.. Waiting to retry')
        r = requests.get(BOMURL)        
    except requests.exceptions.TooManyRedirects:
        print('URL is bad and try a different one')
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        # raise SystemExit(e)
        print(e)
        sleep (7200)
        r = requests.get(BOMURL)        
    return r


def convertdata():
    bom_data = pulldatafrombom()
    raw_data = json.loads(bom_data.content.decode())
    location = raw_data['observations']['header'][0]['name'] + ", " + raw_data['observations']['header'][0]['state_time_zone']    
    data_points = []
    for values in raw_data['observations']['data']:
        time_bom = values.get('local_date_time_full')
        for key in values:
            if key in data_points_to_collect:
                x = {"measurement": measurement_name, "tags": {"location": location}, "fields": {key: values.get(key)}, "time": time_bom}
                data_points.append(x)
    return data_points

while True:
    try:
        x = convertdata()
        y = writeinflux.writetodb(data_points=x)
        print("wrote BOM to database successfully")
    except Exception as e:
        print("error with reading and converting data ", e))
        pass
    sleep(1200)



#   File "/usr/src/app/scripts/weather_bom.py", line 43, in convertdata
#     raw_data = json.loads(bom_data.content.decode())
#   File "/usr/local/lib/python3.9/json/decoder.py", line 355, in raw_decode
#     raise JSONDecodeError("Expecting value", s, err.value) from None
# json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)