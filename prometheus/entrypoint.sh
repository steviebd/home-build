#!/bin/sh

# Substitute environment variables in the prometheus config template
envsubst < /etc/prometheus/prometheus.yml.template > /etc/prometheus/prometheus.yml

# Start prometheus with the original arguments
exec /bin/prometheus "$@"
