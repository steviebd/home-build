# Balena Cloud Deployment Guide

## Setup

1. **Create Balena Application**
   ```bash
   balena login
   balena app create home-monitoring-system --type raspberrypi4-64
   ```

2. **Set Environment Variables**
   Configure these in Balena Cloud dashboard or via CLI:
   ```bash
   # InfluxDB Configuration
   balena env add INFLUX_DB_BUCKET "home_monitoring" --application home-monitoring-system
   balena env add INFLUX_DB_TOKEN "your-token-here" --application home-monitoring-system
   balena env add INFLUX_DB_ORG "home" --application home-monitoring-system
   balena env add DEVICE_DB_LOCATION "http://influxdb:8086" --application home-monitoring-system
   
   # InfluxDB Init
   balena env add DOCKER_INFLUXDB_INIT_PASSWORD "admin123" --application home-monitoring-system
   balena env add DOCKER_INFLUXDB_INIT_ORG "home" --application home-monitoring-system
   balena env add DOCKER_INFLUXDB_INIT_BUCKET "home_monitoring" --application home-monitoring-system
   balena env add DOCKER_INFLUXDB_INIT_ADMIN_TOKEN "your-admin-token" --application home-monitoring-system
   
   # Grafana
   balena env add GF_SECURITY_ADMIN_PASSWORD "admin123" --application home-monitoring-system
   ```

3. **Deploy to Balena Cloud**
   ```bash
   balena push home-monitoring-system
   ```

## Device Configuration

The following hardware features are automatically enabled:
- I2C interface for sensor communication
- SPI interface 
- GPIO access for sensors
- RTC module support

## Accessing Services

- **Grafana Dashboard**: Access via device's public URL on port 80
- **InfluxDB**: Internal service on port 8086 (not exposed publicly)

## Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `INFLUX_DB_BUCKET` | InfluxDB bucket name | `home_monitoring` |
| `INFLUX_DB_TOKEN` | InfluxDB access token | Generate in InfluxDB UI |
| `INFLUX_DB_ORG` | InfluxDB organization | `home` |
| `DEVICE_DB_LOCATION` | InfluxDB connection URL | `http://influxdb:8086` |
| `GF_SECURITY_ADMIN_PASSWORD` | Grafana admin password | `admin123` |

## Balena Features Used

- **Privileged containers**: For GPIO/I2C access
- **Volume persistence**: For InfluxDB and Grafana data
- **Host features**: procfs, sysfs for system monitoring
- **Supervisor API**: For container management
