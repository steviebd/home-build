import os
import qwiic_ccs811
from time import sleep
from grafana_cloud_writer import GrafanaCloudPushGateway

# Variables used and inputted into the fuctions
location = os.getenv("DEVICE_DB_LOCATION")
measurement_name = "ccs811"
# startup of sensor so it doesn't just write 0 values
# API Documentation @ https://qwiic-ccs811-py.readthedocs.io/en/latest/apiref.html

mySensor = qwiic_ccs811.QwiicCcs811() 
mySensor.begin()
mySensor.read_algorithm_results()
sleep(30)

def convertdata():
# take the readings and store it on the board so it can be pulled
    mySensor.read_algorithm_results()
# format the data as a single measurement for influx
    co2_level = {"measurement": measurement_name, "tags": {"location": location}, "fields": {"co2": float(mySensor.get_co2())}}
    tvoc_level = {"measurement": measurement_name, "tags": {"location": location}, "fields": {"tVOC": float(mySensor.get_tvoc())}}
# combining into a list
    data_return = [co2_level, tvoc_level]
    return data_return

# Initialize Grafana Cloud writer
cloud_writer = GrafanaCloudPushGateway()

while True:
    x = convertdata()
    cloud_writer.push_metrics("ccs811_sensor", x)
    print("wrote CCS811 to Grafana Cloud successfully")
    sleep(60)