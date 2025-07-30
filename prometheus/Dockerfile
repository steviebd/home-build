FROM prom/prometheus:v2.55.1

# Copy startup script that will generate config with env vars
COPY start.sh /start.sh
USER root
RUN chmod +x /start.sh
USER nobody

ENTRYPOINT ["/start.sh"]
