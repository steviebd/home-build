import qwiic_ccs811
from time import sleep
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import os

# Variables used and inputted into the fuctions
my_bucket = os.getenv("INFLUX_DB_BUCKET")
influx_token = os.getenv("INFLUX_DB_TOKEN")
influx_org = os.getenv("INFLUX_DB_ORG")
location = os.getenv("DEVICE_DB_LOCATION")
measurement_name = "ccs811"
# startup of sensor so it doesn't just write 0 values
# API Documentation @ https://qwiic-ccs811-py.readthedocs.io/en/latest/apiref.html

mySensor = qwiic_ccs811.QwiicCcs811() 
mySensor.begin()
mySensor.read_algorithm_results()
sleep(180)

def sendtoinfluxdb():
    # take the readings and store it on the board so it can be pulled
    mySensor.read_algorithm_results()
    # format the data as a single measurement for influx                
    co2_level = Point(measurement_name).tag("location", location).field("co2", float(mySensor.get_tvoc()))
    tvoc_level = Point(measurement_name).tag("location", location).field("tVOC", float(mySensor.get_co2()))
    #  Write to influxdb
    client = InfluxDBClient(url="http://influxdb:8086", token=influx_token, org=influx_org)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    write_api.write(bucket=my_bucket, record=[co2_level, tvoc_level])
    # Control how often data is written
    client.close()

while True:
    try:
        x = sendtoinfluxdb()
        sleep(200)
    except requests.exceptions.Timeout:
        print('requests.exceptions.Timeout')
        sleep(7200)
        x = sendtoinfluxdb()
    except requests.exceptions.TooManyRedirects:
        print('URL is bad and try a different one')
    except requests.exceptions.ConnectionError:
        sleep(7200)
        print('Connection to the website or database is down.. Waiting to retry')    
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        raise SystemExit(e)