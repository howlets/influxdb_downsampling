import os

# Flask settings
SERVER_NAME = os.getenv('SERVER_NAME', '0.0.0.0')
SERVER_PORT = os.getenv('SERVER_PORT', 8080)
FLASK_THREADED = os.getenv('FLASK_THREADED', True)
FLASK_DEBUG = os.getenv('FLASK_DEBUG', False)

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = os.getenv('RESTPLUS_SWAGGER_UI_DOC_EXPANSION', 'list')
RESTPLUS_VALIDATE = os.getenv('RESTPLUS_VALIDATE', True)
RESTPLUS_MASK_SWAGGER = os.getenv('RESTPLUS_MASK_SWAGGER', False)
RESTPLUS_ERROR_404_HELP = os.getenv('RESTPLUS_ERROR_404_HELP', False)

# Logging
INFLUX_PROXY_LOG = "/var/log/influx_proxy"

LOG_PATH = os.getenv('LOG_PATH', INFLUX_PROXY_LOG)
MONITORING_ELASTIC_NODE = os.getenv('MONITORING_ELASTIC_NODE', '10.200.129.60')
SERVICE_NAME = os.getenv('SERVICE_NAME', 'influx_proxy')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
