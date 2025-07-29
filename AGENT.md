# AGENT.md - Home Weather Monitoring System

## Build/Run Commands
- Build & deploy: `docker-compose up -d` (in /sensor directory)
- View logs: `docker-compose logs sensor` or `docker-compose logs prometheus`
- Test sensor locally: `python3 sensor/sensor/scripts/sensor.py`
- Test metrics endpoint: `curl http://localhost:8000/metrics`

## Architecture & Structure
- **Balena.io IoT project** for Raspberry Pi 4 with environmental sensors (CCS811/BME280)
- **Docker services**: sensor (Python + HTTP metrics server), prometheus (local monitoring + remote_write)
- **Network**: Internal (172.20.0.0/24) + external bridge to private LAN (192.168.1.x)
- **Data flow**: Sensors → Python scripts → Prometheus (local) → Grafana Cloud (remote_write)
- **Environment config**: .env with GRAFANA_CLOUD_PUSH_URL, GRAFANA_CLOUD_USERNAME, GRAFANA_CLOUD_PASSWORD, DEVICE_DB_LOCATION

## Code Style & Conventions
- **Python 3.12** with requirements.txt dependencies (sparkfun-qwiic, influxdb-client, RPi.GPIO)
- **Multiprocessing**: sensor.py imports and runs bme280.py + ccs811.py in parallel processes
- **Environment variables**: Use os.environ or env_file for configuration, never hardcode credentials
- **Docker**: Single-purpose containers, privileged mode for GPIO/I2C access
- **Naming**: snake_case for Python files/variables, descriptive service names in docker-compose
