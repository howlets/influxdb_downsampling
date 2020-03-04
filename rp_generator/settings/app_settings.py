import os
PWD = os.path.dirname(os.path.abspath(__file__))

INFLUXDB_URL = os.getenv('INFLUXDB_URL', 'http://127.0.0.1:8086')
INFLUXDB_USER = os.getenv('INFLUXDB_USER', 'grafana')
INFLUXDB_PASS = os.getenv('INFLUXDB_USER', 'grafana')
RP_CHECK_TIME = os.getenv('RP_CHECK_TIME', 30)
PATH_TO_RP_CONFIG = os.getenv('PATH_TO_RP_CONFIG', '')
