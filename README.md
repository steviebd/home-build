# Raspberry Pi Ad Block and home weather monitoring with dockers

Docker containers running on [Ubuntu Server 20.04.2 LTS](https://ubuntu.com/download/raspberry-pi).

## Pihole with Cloudflare

Using Mr Roach for the detailed [guide](http://mroach.com/2020/08/pi-hole-and-cloudflared-with-docker/#background-and-pre-configuration) on setting up PiHole and Cloudflared DoH networking and understand on how to set it up securely.

[VisiblitySpots](https://github.com/visibilityspots/dockerfile-cloudflared) for the dockerfile to help get Cloudflare DoH working on a Raspberry Pi 4.

Cloudflare has been set to only communicate with PiHole with a seperate network and flow using Docker 
```
macvlan
```

Please read through Mr Roach's excellent explination on it and how to set it up in your environment.

Once done make sure to change your:
```
        priv_lan:
                ipv4_address: 192.168.1.200
```

To something in your network. You can then access the PiHole dashboard at xxx.xxx.x.xxx/admin.

## Home Weather Monitoring

Built on Raspberry Pi 4 with the [SparkFun Environmental Combo Breakout - CCS811/BME280 (Qwiic)](https://github.com/sparkfun/Qwiic_BME280_CCS811_Combo) on Python.

Using [Balena.io](http://balena.io/) who provide a full technology stack develop, deploy, and manage projects at any scale; all on the cloud.

Pihole + unbound copied from [klutchell](https://github.com/klutchell/balena-pihole).

pHAT Shutown button copied from [sparkfun reboot and shutdown guide](https://learn.sparkfun.com/tutorials/raspberry-pi-safe-reboot-and-shutdown-button/all).

## Enviromental Variables Used

Add a database.env file and input the following details

    - DEVICE_DB_LOCATION = The device location
    - INFLUX_DB_BUCKET = The bucket name for Influx DB
    - INFLUX_DB_TOKEN = Token generated from Influx DB. More infomration can be found at [InfluxDB's documentation](https://docs.influxdata.com/influxdb/v2.0/security/tokens/)
    - INFLUX_DB_ORG = The organisation ID for your bucket

Sensor uses Python and [influxdb-client-python](https://github.com/influxdata/influxdb-client-python) libaries to write into influxdb.


## Setup of initial persistant InfluxDB database and users

You will need to change your InfluxDB external address in the docker-compose.yml file to match your internal network settings.

```
        priv_lan:
                ipv4_address: 192.168.1.191
```

You can then access the InfluxDB database @ xxx.xxx.x.xxx:8086.

Setup details can be found [here](https://docs.influxdata.com/influxdb/v2.0/reference/cli/influx/setup/) and the easiest way is to open up the influxdb url @ http://deviceIP:8086 and follow the intial setup prompts.

Alternatively you can open up a CLI terminal on the docker and type in:

    influx setup 

and follow the prompts.

## Setup of scripts for the sensor

You will need to change your Sensor external address in the docker-compose.yml file to match your internal network settings.

``` 
        priv_lan:
                ipv4_address: 192.168.1.192
```

Environmental files would need to be added. Default is 'database.env' on the composer

The following fields are needed:

    - INFLUX_DB_BUCKET: ${Your influxdb bucket that was setup}
    - INFLUX_DB_TOKEN: ${Your influxdb token} 
    - INFLUX_DB_ORG: ${Your influxdb organisation name}
    - DEVICE_DB_LOCATION: ${Input flag to filter by location of devices}

Alternatively you can go into the Python scripts and hardcode these values in directly.

Scripts needed are:

    - bme280.py
    - ccs811.py
    - weather_bom.py

Finally under weather_bom.py / BOMURL please point the URL to your local data feed under [Observations - Individual Stations](http://www.bom.gov.au/catalogue/data-feeds.shtml) as these feeds provide the necessary .json files which this is written in to accept.

## Setup of Grafana

A template dashboard will be in place with some of the datapoints. Follow the [instructions here](https://grafana.com/docs/grafana/latest/datasources/influxdb/) to connect Grafana to Influx DB via Flux.

Queries can only be made with Flux and not the older InfluxQL.
