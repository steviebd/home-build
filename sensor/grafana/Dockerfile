FROM balenalib/raspberrypi4-64-node:16-run

# Install Grafana
RUN install_packages curl gnupg2 software-properties-common

# Add Grafana repository and install
RUN curl https://packages.grafana.com/gpg.key | apt-key add - && \
    echo "deb https://packages.grafana.com/oss/deb stable main" > /etc/apt/sources.list.d/grafana.list && \
    apt-get update && \
    install_packages grafana

# Copy custom provisioning
COPY provisioning /etc/grafana/provisioning

# Create grafana user and set permissions
RUN mkdir -p /var/lib/grafana && \
    chown -R grafana:grafana /var/lib/grafana /etc/grafana

# Switch to grafana user
USER grafana

# Expose Grafana port
EXPOSE 3000

# Start Grafana
CMD ["/usr/sbin/grafana-server", "--homepath=/usr/share/grafana", "--config=/etc/grafana/grafana.ini", "cfg:default.paths.data=/var/lib/grafana", "cfg:default.paths.logs=/var/log/grafana", "cfg:default.paths.plugins=/var/lib/grafana/plugins"]