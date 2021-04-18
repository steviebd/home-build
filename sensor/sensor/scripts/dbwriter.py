import os
from influxdb_client import InfluxDBClient, Point, WriteOptions

# Variables used and inputted into the fuctions
my_bucket = os.getenv("INFLUX_DB_BUCKET")
influx_token = os.getenv("INFLUX_DB_TOKEN")
influx_org = os.getenv("INFLUX_DB_ORG")
influx_url = "http://influxdb:8086"

class writeinflux:
    def writetodb(data_points):

        client = InfluxDBClient(
            url=influx_url,
            token=influx_token,
            org=influx_org
        )
        try:
            data_write = client.write_api(write_options=WriteOptions(batch_size=500,
                                                         flush_interval=10_000,
                                                          jitter_interval=2_000,
                                                          retry_interval=5_000,
                                                          max_retries=5,
                                                          max_retry_delay=30_000,
                                                          exponential_base=2)
            )
            data_write.write(my_bucket, influx_org, data_points)
            print("data written")

        except requests.exceptions.RequestException as e:
    # catastrophic error. bail.
            raise SystemExit(e)
    # Close the connection to the InfluxDB
        client.close()

