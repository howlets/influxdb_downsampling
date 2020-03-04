import yaml
import rp_generator.settings as settings

if settings.PATH_TO_RP_CONFIG == '':
	print(
		"Please specify full path to your retention policy config. Example: export PATH_TO_RP_CONFIG=/opt/rp_config.yaml.\n"
		"More details about this config you can find in documentation - https://github.com/howlets/influxdb_downsampling"
	)
	exit(1)

try:
	with open(settings.PATH_TO_RP_CONFIG) as f:
		RP_CONFIG = yaml.load(f, Loader=yaml.FullLoader)
except FileNotFoundError as err:
	print(f"Message: Can`t find config - {settings.PATH_TO_RP_CONFIG}\nERROR: {err}")
	exit(1)
