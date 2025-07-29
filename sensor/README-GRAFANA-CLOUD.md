# Grafana Cloud Migration

This system has been refactored to send metrics directly to Grafana Cloud instead of using local InfluxDB and Grafana instances.

## Setup

1. **Get Grafana Cloud credentials:**
   - Sign up for Grafana Cloud at https://grafana.com/
   - Go to your Grafana Cloud Portal
   - Click on "Prometheus" card then "Details"
   - Copy the Push URL, Username, and Password

2. **Configure environment:**
   ```bash
   cp grafana-cloud.env.example grafana-cloud.env
   # Edit grafana-cloud.env with your actual credentials
   ```

3. **Deploy:**
   ```bash
   docker-compose -f docker-compose-cloud.yml up -d
   ```

## Changes Made

- **Removed services:** InfluxDB, Grafana, and Telegraf containers
- **New writer:** Created `grafana_cloud_writer.py` to send metrics in Prometheus format
- **Updated sensors:** Modified `bme280.py` and `ccs811.py` to use Grafana Cloud writer
- **Simplified networking:** Only requires external network connection

## Metrics Format

Metrics are sent in Prometheus format:
- `bme280_humidity{location="home"} 45.2`
- `bme280_pressure{location="home"} 1013.25`
- `ccs811_co2{location="home"} 400`
- `ccs811_tvoc{location="home"} 10`

## Original Setup

To use the original local setup, use:
```bash
docker-compose up -d
```

## Troubleshooting

- Check container logs: `docker-compose -f docker-compose-cloud.yml logs sensor`
- Verify environment variables are set correctly
- Check Grafana Cloud status page for service availability
