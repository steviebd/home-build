#!/bin/sh

# Create prometheus config with environment variables
cat > /etc/prometheus/prometheus.yml << EOF
global:
  scrape_interval: 60s
  external_labels:
    origin_prometheus: 'home-monitoring'
    location: '${DEVICE_DB_LOCATION:-unknown}'

remote_write:
  - url: ${GRAFANA_CLOUD_PUSH_URL}
    basic_auth:
      username: ${GRAFANA_CLOUD_USERNAME}
      password: ${GRAFANA_CLOUD_PASSWORD}

scrape_configs:
  # Scrape Prometheus itself
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  # Scrape sensor metrics
  - job_name: 'home-sensors'
    scrape_interval: 30s
    static_configs:
      - targets: ['sensor:8000']
    metrics_path: '/metrics'
EOF

# Start prometheus with the original arguments
exec /bin/prometheus "$@"
