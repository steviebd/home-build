import os
import qwiic_ccs811
from time import sleep
from metrics_server import update_metrics

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
# format the data as a single measurement for prometheus
    co2_level = {"measurement": measurement_name, "tags": {"location": location}, "fields": {"co2": float(mySensor.get_co2())}}
    tvoc_level = {"measurement": measurement_name, "tags": {"location": location}, "fields": {"tVOC": float(mySensor.get_tvoc())}}
# combining into a list
    data_return = [co2_level, tvoc_level]
    return data_return

while True:
    x = convertdata()
    update_metrics("ccs811", x)
    print("updated CCS811 metrics for Prometheus")
    sleep(60)