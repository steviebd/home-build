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
    except requests.exceptions.TooManyRedirects:
        print('URL is bad and try a different one')
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        raise SystemExit(e)
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
    x = convertdata()
    y = writeinflux.writetodb(data_points=x)
    print("wrote to database successfully")
    sleep(600)
