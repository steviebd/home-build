FROM alpine:latest AS config-builder
RUN apk add --no-cache gettext

FROM prom/prometheus:v2.55.1

# Copy envsubst from alpine
COPY --from=config-builder /usr/bin/envsubst /usr/bin/envsubst

# Copy the template and create an entrypoint script
COPY prometheus.yml.template /etc/prometheus/prometheus.yml.template
COPY entrypoint.sh /entrypoint.sh
USER root
RUN chmod +x /entrypoint.sh
USER nobody

ENTRYPOINT ["/entrypoint.sh"]
