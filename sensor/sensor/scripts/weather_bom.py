from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import os
import requests
import json
from time import sleep

# Variables used and inputted into the fuctions
my_bucket = os.getenv("INFLUX_DB_BUCKET")
influx_token = os.getenv("INFLUX_DB_TOKEN")
influx_org = os.getenv("INFLUX_DB_ORG")
measurement_name = "BOM Weather"
# Measurements from the BOM URL to pull and input.
data_points_to_collect = ('gust_kmh', 'air_temp', 'dewpt', 'press', 'rel_hum', 'wind_spd_kmh')

# Datafeed from http://www.bom.gov.au/catalogue/data-feeds.shtml under Observations - individual stations for .json files
BOMURL = 'http://reg.bom.gov.au/fwo/IDN60901/IDN60901.94765.json'

def pulldatafrombom():
    try:
        r = requests.get(BOMURL)
    except requests.exceptions.Timeout:
        print('requests.exceptions.Timeout')
        sleep(7200)
        r = requests.get(BOMURL)
    except requests.exceptions.TooManyRedirects:
        print('URL is bad and try a different one')
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        raise SystemExit(e)
    data = json.loads(r.content.decode())
    return data

def sendtoinfluxdb():
    data = pulldatafrombom()
    location = data['observations']['header'][0]['name'] + ", " + data['observations']['header'][0]['state_time_zone']
    client = InfluxDBClient(
        url='http://influxdb:8086',
        token=influx_token,
        org=influx_org
    )
    write_api = client.write_api(write_options=SYNCHRONOUS)
    for values in data['observations']['data']:
        time_bom = values.get('local_date_time_full')
        for key in values:
            if key in data_points_to_collect:
                data =  Point(measurement_name).tag('location', location).field(key, values.get(key)).time(time_bom)
                write_api.write(bucket=my_bucket, record=data)
    client.close()

while True:
    try:
        sendtoinfluxdb()
        sleep(600)
    except ConnectionError as e:
        print(e)
        slee(7200)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    try:
        sendtoinfluxdb()
    except Exception as e:
        print(e)
