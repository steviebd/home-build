FROM balenalib/raspberrypi4-64-debian:bullseye-run

# Enable systemd init system
ENV INITSYSTEM on

# Install system dependencies for I2C and GPIO
RUN install_packages i2c-tools python3-dev gcc python3-pip

# Set working directory
WORKDIR /usr/src/app

# Copy requirements and install Python dependencies
COPY ./requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application scripts
COPY ./scripts ./scripts

# Enable I2C interface
RUN echo 'i2c-dev' >> /etc/modules

# Start the sensor application
CMD ["python3", "/usr/src/app/scripts/sensor.py"] 