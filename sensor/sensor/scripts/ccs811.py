#!/usr/bin/env python3
import os
import random
import time
import sys

# Force unbuffered output
sys.stdout.flush()
sys.stderr.flush()

# Configuration
measurement_name = "ccs811"
location = os.getenv("DEVICE_DB_LOCATION", "home")

def generate_mock_data():
    """Generate realistic mock sensor data"""
    return [
        {"measurement": measurement_name, "tags": {"location": location, "data_source": "mock"}, "fields": {"co2": round(random.uniform(400, 1200), 2)}},
        {"measurement": measurement_name, "tags": {"location": location, "data_source": "mock"}, "fields": {"tVOC": round(random.uniform(0, 500), 2)}}
    ]

def generate_real_data(sensor):
    """Generate data from real CCS811 sensor"""
    sensor.read_algorithm_results()
    return [
        {"measurement": measurement_name, "tags": {"location": location, "data_source": "hardware"}, "fields": {"co2": float(sensor.get_co2())}},
        {"measurement": measurement_name, "tags": {"location": location, "data_source": "hardware"}, "fields": {"tVOC": float(sensor.get_tvoc())}}
    ]

if __name__ == "__main__":
    print("CCS811 sensor script starting", flush=True)
    
    # Check if we're on a Raspberry Pi by looking for I2C device
    device_status = os.path.exists("/dev/i2c-1")
    mySensor = None
    
    # Initialize sensor (real or mock)
    if device_status:
        try:
            import qwiic_ccs811
            mySensor = qwiic_ccs811.QwiicCcs811()
            mySensor.begin()
            mySensor.read_algorithm_results()
            time.sleep(30)
            print("CCS811 hardware sensor initialized successfully", flush=True)
        except Exception as e:
            print(f"CCS811 sensor initialization failed ({e}), using mock data", flush=True)
            device_status = False
            mySensor = None
    else:
        print("CCS811 using mock data (no I2C device detected)", flush=True)
    
    # Import after prints to ensure they show up
    from metrics_server import update_metrics
    print("CCS811 metrics_server imported successfully", flush=True)
    
    while True:
        try:
            if device_status and mySensor:
                data = generate_real_data(mySensor)
                print("Generated CCS811 hardware data", flush=True)
            else:
                data = generate_mock_data()
                print("Generated CCS811 mock data", flush=True)
            update_metrics("ccs811", data)
            print("Updated CCS811 metrics for Prometheus", flush=True)
            time.sleep(30)  # Update every 30 seconds
        except Exception as e:
            print(f"Error in CCS811 loop: {e}", flush=True)
            time.sleep(5)  # Wait before retrying
