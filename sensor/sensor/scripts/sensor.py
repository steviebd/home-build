from multiprocessing import Process
# Run all python scripts at the same time

def one(): import bme280
def two(): import ccs811
def three(): import top_phat_button
def four(): import weather_bom

Process(target=one).start()
Process(target=two).start()
Process(target=three).start()
Process(target=four).start()