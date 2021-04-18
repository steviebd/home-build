from multiprocessing import Process
# Run all python scripts at the same time
from time import sleep

def one(): import bme280
def two(): import ccs811
def three(): import top_phat_button
def four(): import weather_bom
# Sleep function used to ensure that the influxDB is up and running as containers may face issues with write
# sleep(60)
Process(target=one).start()
Process(target=two).start()
Process(target=three).start()
Process(target=four).start()