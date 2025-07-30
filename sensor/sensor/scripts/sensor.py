from multiprocessing import Process
from metrics_server import start_metrics_server
import time

# Start the metrics server for Prometheus scraping
print("Starting metrics server...")
metrics_server = start_metrics_server(port=8000)

# Give the server a moment to start
time.sleep(2)

# Run all python scripts at the same time
def one(): 
    import subprocess
    subprocess.run(["python3", "/usr/src/app/scripts/bme280.py"])

def two(): 
    import subprocess
    subprocess.run(["python3", "/usr/src/app/scripts/ccs811.py"])

print("Starting sensor processes...")
p1 = Process(target=one)
p2 = Process(target=two)
p1.start()
p2.start()

print("Sensor monitoring system started - metrics available at :8000/metrics")

# Keep the main process alive
try:
    while True:
        time.sleep(60)
        # Check if processes are still alive
        if not p1.is_alive():
            print("BME280 process died, restarting...")
            p1 = Process(target=one)
            p1.start()
        if not p2.is_alive():
            print("CCS811 process died, restarting...")
            p2 = Process(target=two)
            p2.start()
except KeyboardInterrupt:
    print("Shutting down...")
    p1.terminate()
    p2.terminate()
    p1.join()
    p2.join()