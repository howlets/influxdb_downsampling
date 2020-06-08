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
LOG_PATH = os.getenv('LOG_PATH', '/var/log/influx-rp-generator')
SERVICE_NAME = os.getenv('SERVICE_NAME', 'influx-rp-generator')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
