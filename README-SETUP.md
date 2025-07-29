# Home Weather Monitoring System - Setup Guide

This Balena.io IoT project monitors environmental conditions using CCS811/BME280 sensors on Raspberry Pi 4.

## Quick Start

1. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your preferred setup (see options below)
   ```

2. **Choose deployment mode:**
   
   **Grafana Cloud (Recommended):**
   ```bash
   docker-compose --profile cloud up -d
   ```
   
   **Local Infrastructure:**
   ```bash
   docker-compose --profile local up -d
   ```

## Setup Options

### Option 1: Grafana Cloud (Recommended)
- ✅ No local infrastructure needed
- ✅ Automatic scaling and maintenance
- ✅ Remote access to dashboards
- ✅ Built-in alerting

**Requirements:**
- Grafana Cloud account (free tier available)
- Internet connection for metric push

**Configuration:**
1. Sign up at https://grafana.com/
2. Go to Cloud Portal > Prometheus card > Details
3. Copy credentials to `.env` file

### Option 2: Local Infrastructure (Legacy)
- ✅ Full data control
- ❌ Requires local InfluxDB/Grafana setup
- ❌ Manual maintenance required

**Services included:**
- InfluxDB 2.0.4 (time-series database)
- Grafana 7.5.4 (visualization)
- Telegraf (system metrics)

## Commands

**View logs:**
```bash
docker-compose logs sensor
```

**Restart services:**
```bash
docker-compose --profile cloud restart
```

**Clean stop:**
```bash
docker-compose down
```

## Metrics Generated

**BME280 Environmental Sensor:**
- `bme280_humidity{location="home"}` - Humidity percentage
- `bme280_pressure{location="home"}` - Atmospheric pressure
- `bme280_celsius{location="home"}` - Temperature in Celsius
- `bme280_dewpoint_celsius{location="home"}` - Dew point

**CCS811 Air Quality Sensor:**
- `ccs811_co2{location="home"}` - CO2 levels (ppm)
- `ccs811_tvoc{location="home"}` - Total Volatile Organic Compounds

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   BME280/CCS811 │───▶│  Raspberry Pi    │───▶│  Grafana Cloud  │
│     Sensors     │    │   (Docker)       │    │   OR Local DB   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## Troubleshooting

**Sensor not detected:**
- Check I2C is enabled: `sudo raspi-config`
- Verify wiring connections
- Check container logs: `docker-compose logs sensor`

**Network issues:**
- Verify `priv_lan` network exists
- Check firewall settings
- For cloud setup: verify internet connectivity

**Permission issues:**
- Ensure Docker daemon is running
- Check user is in docker group: `sudo usermod -aG docker $USER`
