import yaml
import os


PATH_TO_RP_CONFIG = os.getenv('PATH_TO_RP_CONFIG', f'/opt/influx-rp-generator/rp_config.yaml')
PWD = os.path.dirname(os.path.abspath(__file__))


if PATH_TO_RP_CONFIG == '':
	print(
		"Please specify full path to your retention policy config. Example: export PATH_TO_RP_CONFIG=/opt/rp_config.yaml.\n"
		"More details about this config you can find in documentation - https://github.com/howlets/influxdb_downsampling"
	)
	exit(1)

try:
	with open(PATH_TO_RP_CONFIG) as f:
		RP_CONFIG = yaml.load(f, Loader=yaml.FullLoader)
except FileNotFoundError as err:
	print(f"Message: Can`t find config - {PATH_TO_RP_CONFIG}\nERROR: {err}")
	exit(1)
