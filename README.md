# Home Weather Monitoring System

IoT environmental monitoring using BME280/CCS811 sensors on Raspberry Pi 4 with Grafana Cloud integration.

## Quick Start

```bash
# Configure environment
cp .env.example .env
# Edit .env with your Grafana Cloud credentials

# Deploy
docker-compose up -d
```

## Hardware

- **Raspberry Pi 4** with I2C enabled
- **[SparkFun Environmental Combo Breakout - CCS811/BME280 (Qwiic)](https://github.com/sparkfun/Qwiic_BME280_CCS811_Combo)**
- **Optional:** pHAT shutdown button

## Deployment Options

### Grafana Cloud
✅ No local infrastructure • ✅ Remote access • ✅ Built-in alerting • ✅ Automatic scaling

1. Sign up at https://grafana.com (free tier available)
2. Get credentials: Cloud Portal > Prometheus > Details
3. Add to `.env`: `GRAFANA_CLOUD_PUSH_URL`, `GRAFANA_CLOUD_USERNAME`, `GRAFANA_CLOUD_PASSWORD`

### Balena Cloud
✅ Fleet management • ✅ OTA updates • ✅ Remote monitoring

```bash
balena login
balena app create home-monitoring --type raspberrypi4-64
balena push home-monitoring
```

Set environment variables in Balena dashboard or via CLI.

## Metrics

**Environmental (BME280):**
- `bme280_humidity` - Humidity %
- `bme280_pressure` - Atmospheric pressure  
- `bme280_celsius` - Temperature °C
- `bme280_dewpoint_celsius` - Dew point

**Air Quality (CCS811):**
- `ccs811_co2` - CO2 levels (ppm)
- `ccs811_tvoc` - Total VOCs

All metrics include `location` tag for filtering.

## Configuration

**Required Environment Variables:**
```bash
# Device location tag
DEVICE_DB_LOCATION=home

# Grafana Cloud
GRAFANA_CLOUD_PUSH_URL=https://prometheus-prod-XX.grafana.net/api/prom/push
GRAFANA_CLOUD_USERNAME=your_username  
GRAFANA_CLOUD_PASSWORD=your_password
```

## Commands

```bash
# View logs
docker-compose logs sensor

# Restart
docker-compose restart

# Stop
docker-compose down
```

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   BME280/CCS811 │───▶│  Raspberry Pi    │───▶│  Grafana Cloud  │
│     Sensors     │    │   (Docker)       │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## Troubleshooting

**Sensor issues:**
- Enable I2C: `sudo raspi-config` > Interface > I2C
- Check wiring and power
- View logs: `docker-compose logs sensor`

**Network issues:**
- Verify `priv_lan` network exists
- Check internet connectivity for Grafana Cloud
- Ensure Docker daemon is running

**Balena deployment:**
- Privileged containers enabled for GPIO/I2C access
- Host features: procfs, sysfs for system monitoring

---

*Built with Python 3.12, Docker, and [Balena.io](https://balena.io) platform. Based on [influxdb-client-python](https://github.com/influxdata/influxdb-client-python) and SparkFun Qwiic libraries.*
