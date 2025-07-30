#!/usr/bin/env python3
import os
import random
import time
import sys

# Force unbuffered output
sys.stdout.flush()
sys.stderr.flush()

# Configuration
measurement_name = "bme280"
location = os.getenv("DEVICE_DB_LOCATION", "home")

def generate_mock_data():
    """Generate realistic mock sensor data"""
    return [
        {"measurement": measurement_name, "tags": {"location": location, "data_source": "mock"}, "fields": {"Humidity": round(random.uniform(40, 70), 2)}},
        {"measurement": measurement_name, "tags": {"location": location, "data_source": "mock"}, "fields": {"Pressure": round(random.uniform(1000, 1030), 2)}},
        {"measurement": measurement_name, "tags": {"location": location, "data_source": "mock"}, "fields": {"Dewpoint celsius": round(random.uniform(15, 25), 2)}},
        {"measurement": measurement_name, "tags": {"location": location, "data_source": "mock"}, "fields": {"Celsius": round(random.uniform(20, 30), 2)}}
    ]

def generate_real_data(sensor):
    """Generate data from real BME280 sensor"""
    return [
        {"measurement": measurement_name, "tags": {"location": location, "data_source": "hardware"}, "fields": {"Humidity": float(sensor.humidity)}},
        {"measurement": measurement_name, "tags": {"location": location, "data_source": "hardware"}, "fields": {"Pressure": float(sensor.pressure)}},
        {"measurement": measurement_name, "tags": {"location": location, "data_source": "hardware"}, "fields": {"Dewpoint celsius": float(sensor.dewpoint_celsius)}},
        {"measurement": measurement_name, "tags": {"location": location, "data_source": "hardware"}, "fields": {"Celsius": float(sensor.temperature_celsius)}}
    ]

if __name__ == "__main__":
    print("BME280 sensor script starting", flush=True)
    
    # Check if we're on a Raspberry Pi by looking for I2C device
    device_status = os.path.exists("/dev/i2c-1")
    mySensor = None
    
    # Initialize sensor (real or mock)
    if device_status:
        try:
            import qwiic_bme280
            mySensor = qwiic_bme280.QwiicBme280()
            mySensor.begin()
            time.sleep(5)
            print("BME280 hardware sensor initialized successfully", flush=True)
        except Exception as e:
            print(f"BME280 sensor initialization failed ({e}), using mock data", flush=True)
            device_status = False
            mySensor = None
    else:
        print("BME280 using mock data (no I2C device detected)", flush=True)
    
    # Import after prints to ensure they show up
    from metrics_server import update_metrics
    print("BME280 metrics_server imported successfully", flush=True)
    
    while True:
        try:
            if device_status and mySensor:
                data = generate_real_data(mySensor)
                print("Generated BME280 hardware data", flush=True)
            else:
                data = generate_mock_data()
                print("Generated BME280 mock data", flush=True)
            update_metrics("bme280", data)
            print("Updated BME280 metrics for Prometheus", flush=True)
            time.sleep(30)  # Update every 30 seconds
        except Exception as e:
            print(f"Error in BME280 loop: {e}", flush=True)
            time.sleep(5)  # Wait before retrying
