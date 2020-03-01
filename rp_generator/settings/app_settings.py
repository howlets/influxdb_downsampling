import os

INFLUXDB_URL = os.getenv('INFLUXDB_URL', 'http://127.0.0.1:8086')
INFLUXDB_USER = os.getenv('INFLUXDB_USER', 'grafana')
INFLUXDB_PASS = os.getenv('INFLUXDB_USER', 'grafana')
INFLUXDB_DEFAULT_POLICY = os.getenv('INFLUXDB_DEFAULT_POLICY', 'autogen')
INFLUXDB_RP = os.getenv('INFLUXDB_RP', {'long_term': '48w_5m'})


# CONFIG = {
#     'influxdb_http': 'http://127.0.0.1:8086',
#     'influx_user': 'grafana',
#     'influx_pass': 'grafana',
#     'default_rp': 'autogen',
#     'rp_mapping': {
#         '2592000': 'autogen',
#         '31104000': '48w_5m'
#     }
# }