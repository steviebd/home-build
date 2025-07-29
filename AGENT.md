# AGENT.md - Home Weather Monitoring System

## Build/Run Commands
- Build & deploy: `docker-compose up -d` (in /sensor directory)
- Run individual container: `docker-compose up <service_name>` (sensor, influxdb, grafana, telegraf)
- View logs: `docker-compose logs <service_name>`
- Test sensor locally: `python3 sensor/sensor/scripts/sensor.py`

## Architecture & Structure
- **Balena.io IoT project** for Raspberry Pi 4 with environmental sensors (CCS811/BME280)
- **Docker services**: sensor (Python), InfluxDB (time-series DB), Grafana (dashboards), Telegraf (metrics)
- **Network**: Internal (175.40.9.0/29) + external bridge to private LAN (192.168.1.x)
- **Data flow**: Sensors → Python scripts → InfluxDB → Grafana visualization
- **Environment config**: database.env with INFLUX_DB_BUCKET, INFLUX_DB_TOKEN, INFLUX_DB_ORG, DEVICE_DB_LOCATION

## Code Style & Conventions
- **Python 3.9** with requirements.txt dependencies (sparkfun-qwiic, influxdb-client, RPi.GPIO)
- **Multiprocessing**: sensor.py imports and runs bme280.py + ccs811.py in parallel processes
- **Environment variables**: Use os.environ or env_file for configuration, never hardcode credentials
- **Docker**: Single-purpose containers, privileged mode for GPIO/I2C access
- **Naming**: snake_case for Python files/variables, descriptive service names in docker-compose
