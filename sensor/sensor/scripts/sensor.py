from multiprocessing import Process
from metrics_server import start_metrics_server
import time

# Start the metrics server for Prometheus scraping
print("Starting metrics server...")
metrics_server = start_metrics_server(port=8000)

# Give the server a moment to start
time.sleep(2)

# Run all python scripts at the same time
def one(): import bme280
def two(): import ccs811
# def four(): import top_phat_button

print("Starting sensor processes...")
Process(target=one).start()
Process(target=two).start()
# Process(target=four).start()

print("Sensor monitoring system started - metrics available at :8000/metrics")