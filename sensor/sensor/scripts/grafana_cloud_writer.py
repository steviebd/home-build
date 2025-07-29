import os
import time
import requests
from datetime import datetime


class GrafanaCloudWriter:
    def __init__(self):
        self.metrics_url = os.getenv("GRAFANA_CLOUD_METRICS_URL")
        self.metrics_username = os.getenv("GRAFANA_CLOUD_METRICS_USERNAME") 
        self.metrics_password = os.getenv("GRAFANA_CLOUD_METRICS_PASSWORD")
        self.location = os.getenv("DEVICE_DB_LOCATION", "home")
        
        if not all([self.metrics_url, self.metrics_username, self.metrics_password]):
            raise ValueError("Missing required Grafana Cloud environment variables")

    def write_metrics(self, measurement, metrics_data):
        """
        Write metrics to Grafana Cloud in Prometheus format
        
        Args:
            measurement: sensor type (e.g., 'bme280', 'ccs811')
            metrics_data: list of metric dictionaries with 'fields' containing metric values
        """
        prometheus_metrics = []
        timestamp_ms = int(time.time() * 1000)
        
        for data_point in metrics_data:
            fields = data_point.get('fields', {})
            for metric_name, value in fields.items():
                # Convert metric name to Prometheus format (lowercase, underscores)
                prom_metric_name = f"{measurement}_{metric_name.lower().replace(' ', '_').replace('(', '').replace(')', '')}"
                
                # Create Prometheus metric line
                metric_line = f'{prom_metric_name}{{location="{self.location}"}} {value} {timestamp_ms}'
                prometheus_metrics.append(metric_line)
        
        # Send metrics to Grafana Cloud
        if prometheus_metrics:
            self._send_to_grafana_cloud('\n'.join(prometheus_metrics))

    def _send_to_grafana_cloud(self, metrics_payload):
        """Send metrics to Grafana Cloud Prometheus endpoint"""
        try:
            response = requests.post(
                self.metrics_url,
                auth=(self.metrics_username, self.metrics_password),
                headers={
                    'Content-Type': 'application/x-protobuf',
                    'Content-Encoding': 'snappy',
                    'X-Prometheus-Remote-Write-Version': '0.1.0'
                },
                data=self._encode_prometheus_remote_write(metrics_payload),
                timeout=30
            )
            
            if response.status_code == 200:
                print("Metrics successfully sent to Grafana Cloud")
            else:
                print(f"Failed to send metrics: {response.status_code} - {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"Error sending metrics to Grafana Cloud: {e}")

    def _encode_prometheus_remote_write(self, metrics_text):
        """
        Simple implementation - for production use, implement proper Prometheus remote write protocol
        For now, we'll use a simpler HTTP approach via the push gateway pattern
        """
        # Convert to simple format for HTTP push
        return metrics_text.encode('utf-8')


# Alternative simpler implementation using HTTP push gateway pattern
class GrafanaCloudPushGateway:
    def __init__(self):
        self.push_url = os.getenv("GRAFANA_CLOUD_PUSH_URL")  # Push gateway URL
        self.username = os.getenv("GRAFANA_CLOUD_USERNAME")
        self.password = os.getenv("GRAFANA_CLOUD_PASSWORD")
        self.location = os.getenv("DEVICE_DB_LOCATION", "home")
        
    def push_metrics(self, job_name, metrics_data):
        """Push metrics using simple HTTP format"""
        metrics_lines = []
        
        for data_point in metrics_data:
            measurement = data_point.get('measurement', 'unknown')
            fields = data_point.get('fields', {})
            
            for metric_name, value in fields.items():
                # Format as Prometheus metric
                safe_metric = metric_name.lower().replace(' ', '_').replace('(', '').replace(')', '')
                metric_line = f'{measurement}_{safe_metric}{{location="{self.location}"}} {value}'
                metrics_lines.append(metric_line)
        
        if metrics_lines:
            self._push_to_gateway(job_name, '\n'.join(metrics_lines))
    
    def _push_to_gateway(self, job, payload):
        """Push to Grafana Cloud using HTTP"""
        url = f"{self.push_url}/metrics/job/{job}"
        
        try:
            response = requests.post(
                url,
                auth=(self.username, self.password),
                headers={'Content-Type': 'text/plain'},
                data=payload,
                timeout=30
            )
            
            if response.status_code in [200, 202]:
                print(f"Metrics pushed successfully for job {job}")
            else:
                print(f"Failed to push metrics: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"Error pushing metrics: {e}")
