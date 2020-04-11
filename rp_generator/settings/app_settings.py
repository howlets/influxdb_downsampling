import os

INFLUXDB_URL = os.getenv('INFLUXDB_URL', 'http://192.168.1.33:8086')
INFLUXDB_USER = os.getenv('INFLUXDB_USER', 'grafana')
INFLUXDB_PASS = os.getenv('INFLUXDB_PASS', 'grafana')
RP_CHECK_TIME = os.getenv('RP_CHECK_TIME', 30)

