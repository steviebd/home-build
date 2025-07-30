import os
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

class MetricsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/metrics':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain; version=0.0.4; charset=utf-8')
            self.end_headers()
            
            # Get current metrics from global storage
            metrics_output = self.get_prometheus_metrics()
            self.wfile.write(metrics_output.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    
    def get_prometheus_metrics(self):
        """Generate Prometheus format metrics from stored sensor data"""
        import json
        import fcntl
        
        # Read metrics from shared file
        latest_metrics = {}
        metrics_file = '/tmp/sensor_metrics.json'
        try:
            with open(metrics_file, 'r') as f:
                fcntl.flock(f.fileno(), fcntl.LOCK_SH)
                latest_metrics = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Use empty dict if file doesn't exist
            pass  # latest_metrics is already initialized as {}
        except Exception as e:
            print(f"Error reading metrics file: {e}")
            latest_metrics = {}
        
        output = []
        timestamp = int(time.time() * 1000)
        location = os.getenv("DEVICE_DB_LOCATION", "home")
        
        # Add help and type information
        output.append('# HELP bme280_temperature_celsius Temperature from BME280 sensor in Celsius')
        output.append('# TYPE bme280_temperature_celsius gauge')
        output.append('# HELP bme280_humidity_percent Humidity from BME280 sensor in percent')
        output.append('# TYPE bme280_humidity_percent gauge')
        output.append('# HELP bme280_pressure_hpa Atmospheric pressure from BME280 sensor in hPa')
        output.append('# TYPE bme280_pressure_hpa gauge')
        output.append('# HELP bme280_dewpoint_celsius Dew point from BME280 sensor in Celsius')
        output.append('# TYPE bme280_dewpoint_celsius gauge')
        output.append('# HELP ccs811_co2_ppm CO2 level from CCS811 sensor in ppm')
        output.append('# TYPE ccs811_co2_ppm gauge')
        output.append('# HELP ccs811_tvoc_ppb Total VOC from CCS811 sensor in ppb')
        output.append('# TYPE ccs811_tvoc_ppb gauge')
        
        # Add metrics with current values
        job_name = os.getenv("PROMETHEUS_JOB_NAME", "home-sensors")
        if 'bme280' in latest_metrics:
            sensor_data = latest_metrics['bme280']
            metrics = sensor_data.get('metrics', {}) if isinstance(sensor_data, dict) else sensor_data
            tags = sensor_data.get('tags', {}) if isinstance(sensor_data, dict) else {}
            
            # Build label string with all available tags
            labels = f'job="{job_name}",location="{tags.get("location", location)}"'
            if 'data_source' in tags:
                labels += f',data_source="{tags["data_source"]}"'
            
            output.append(f'bme280_temperature_celsius{{{labels}}} {metrics.get("Celsius", 0)} {timestamp}')
            output.append(f'bme280_humidity_percent{{{labels}}} {metrics.get("Humidity", 0)} {timestamp}')
            output.append(f'bme280_pressure_hpa{{{labels}}} {metrics.get("Pressure", 0)} {timestamp}')
            output.append(f'bme280_dewpoint_celsius{{{labels}}} {metrics.get("Dewpoint celsius", 0)} {timestamp}')
        
        if 'ccs811' in latest_metrics:
            sensor_data = latest_metrics['ccs811']
            metrics = sensor_data.get('metrics', {}) if isinstance(sensor_data, dict) else sensor_data
            tags = sensor_data.get('tags', {}) if isinstance(sensor_data, dict) else {}
            
            # Build label string with all available tags
            labels = f'job="{job_name}",location="{tags.get("location", location)}"'
            if 'data_source' in tags:
                labels += f',data_source="{tags["data_source"]}"'
            
            output.append(f'ccs811_co2_ppm{{{labels}}} {metrics.get("co2", 0)} {timestamp}')
            output.append(f'ccs811_tvoc_ppb{{{labels}}} {metrics.get("tVOC", 0)} {timestamp}')
        
        return '\n'.join(output) + '\n'

    def log_message(self, format, *args):
        # Suppress HTTP server logs
        pass

# Global storage for latest metrics
latest_metrics = {}

class MetricsServer:
    def __init__(self, port=8000):
        self.port = port
        self.server = None
        self.thread = None
    
    def start(self):
        """Start the metrics server in a background thread"""
        def run_server():
            self.server = HTTPServer(('0.0.0.0', self.port), MetricsHandler)
            print(f"Metrics server starting on port {self.port}")
            self.server.serve_forever()
        
        self.thread = threading.Thread(target=run_server, daemon=True)
        self.thread.start()
    
    def stop(self):
        """Stop the metrics server"""
        if self.server:
            self.server.shutdown()
            self.server.server_close()

def update_metrics(sensor_type, metrics_data):
    """Update the shared metrics storage with new sensor data"""
    import json
    import fcntl
    
    # Convert list of metric dictionaries to combined metrics with tags
    combined_metrics = {}
    combined_tags = {}
    for data_point in metrics_data:
        fields = data_point.get('fields', {})
        tags = data_point.get('tags', {})
        combined_metrics.update(fields)
        combined_tags.update(tags)
    
    # Write to shared file with file locking
    metrics_file = '/tmp/sensor_metrics.json'
    try:
        # Read existing data
        try:
            with open(metrics_file, 'r') as f:
                fcntl.flock(f.fileno(), fcntl.LOCK_SH)
                current_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            current_data = {}
        
        # Update with new data (include both metrics and tags)
        current_data[sensor_type] = {
            'metrics': combined_metrics,
            'tags': combined_tags
        }
        
        # Write back to file
        with open(metrics_file, 'w') as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            json.dump(current_data, f)
            
        print(f"Updated {sensor_type} metrics: {combined_metrics}")
    except Exception as e:
        print(f"Error updating metrics file: {e}")
        # Fallback to in-memory for this process
        global latest_metrics
        latest_metrics[sensor_type] = {
            'metrics': combined_metrics,
            'tags': combined_tags
        }

# Convenience function to start the server
def start_metrics_server(port=8000):
    server = MetricsServer(port)
    server.start()
    return server
