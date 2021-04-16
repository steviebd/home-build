FROM python:3.9.4-buster

# Copy requirements.txt and scripts folder to /usr/src/app
COPY ./scripts /usr/src/app/scripts
COPY ./requirements.txt /usr/src/app
# Install Python package dependencies in requirements.txt
RUN pip3 install --requirement /usr/src/app/requirements.txt
# Start the i2c bus on debian to make sure the CCS811 sensor works
CMD python3 /usr/src/app/scripts/sensor.py
# modprobe i2c-dev && 