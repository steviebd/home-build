import os
import qwiic_bme280
from time import sleep
from dbwriter import writeinflux


# Measurement name to import to the database
measurement_name = "bme280"
location = os.getenv("DEVICE_DB_LOCATION")
# # startup of sensor so it doesn't just write 0 values
# API Docs @ https://qwiic-bme280-py.readthedocs.io/en/latest/?
mySensor = qwiic_bme280.QwiicBme280()
mySensor.begin()
sleep(5)
device_status = False


def convertdata():
# collect and then format the data as a single measurement for influx                     
    humidity_level = {"measurement": measurement_name, "tags": {"location": location}, "fields": {"Humidity": float(mySensor.humidity)}}
    pressure_level = {"measurement": measurement_name, "tags": {"location": location}, "fields": {"Pressure": float(mySensor.pressure)}}
    dewpoint_celsius = {"measurement": measurement_name, "tags": {"location": location}, "fields": {"Dewpoint celsius": float(mySensor.dewpoint_celsius)}}
    temperature_celsius = {"measurement": measurement_name, "tags": {"location": location}, "fields": {"Celsius": float(mySensor.temperature_celsius)}}
# combining into a list
    data_return = [humidity_level, pressure_level, dewpoint_celsius, temperature_celsius]
    return data_return


while True:
    x = convertdata()
    y = writeinflux.writetodb(data_points=x)
    print("wrote to database successfully")
    sleep(20)    