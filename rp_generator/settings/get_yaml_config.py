import yaml
import os
from logger.logging import service_logger

log = service_logger()


PATH_TO_RP_CONFIG = os.getenv('PATH_TO_RP_CONFIG', f'/opt/influx-rp-generator/rp_config.yaml')
PWD = os.path.dirname(os.path.abspath(__file__))


if PATH_TO_RP_CONFIG == '':
	log.error(
		msg="Please specify full path to your retention policy config. Example: export PATH_TO_RP_CONFIG=/opt/rp_config.yaml. More details about this config you can find in documentation - https://github.com/howlets/influxdb_downsampling")
	exit(1)

try:
	with open(PATH_TO_RP_CONFIG) as f:
		RP_CONFIG = yaml.load(f, Loader=yaml.FullLoader)
except FileNotFoundError as err:
	log.error(msg=f"Message: Can`t find config - {PATH_TO_RP_CONFIG}\nERROR: {err}")
	exit(1)
