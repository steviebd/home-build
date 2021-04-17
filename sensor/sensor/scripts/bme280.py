from time import sleep
import qwiic_bme280
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import os
from requests.exceptions import ConnectionError
import requests
# Variables used and inputted into the fuctions
my_bucket = os.getenv("INFLUX_DB_BUCKET")
influx_token = os.getenv("INFLUX_DB_TOKEN")
influx_org = os.getenv("INFLUX_DB_ORG")
location = os.getenv("DEVICE_DB_LOCATION")
measurement_name = "bme280"

# # startup of sensor so it doesn't just write 0 values
# API Docs @ https://qwiic-bme280-py.readthedocs.io/en/latest/?
mySensor = qwiic_bme280.QwiicBme280()
mySensor.begin()


# Connect to client


def sendtoinfluxdb():
    # format the data as a single measurement for influx                     
    humidity_level = Point(measurement_name).tag("location", location).field("Humidity", float(mySensor.humidity))
    pressure_level = Point(measurement_name).tag("location", location).field("Pressure", float(mySensor.pressure))
    dewpoint_celsius = Point(measurement_name).tag("location", location).field("Dewpoint celsius", float(mySensor.dewpoint_celsius))
    temperature_celsius = Point(measurement_name).tag("location", location).field("Celsius", float(mySensor.temperature_celsius))
    #  Write to influxdb
    client = InfluxDBClient(url="http://influxdb:8086", token=influx_token, org=influx_org)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    write_api.write(bucket=my_bucket, record=[humidity_level, pressure_level, dewpoint_celsius, temperature_celsius])
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