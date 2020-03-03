import yaml
import rp_generator.settings as settings


try:
	with open(settings.PATH_TO_RP_CONFIG) as f:
		RP_CONFIG = yaml.load(f, Loader=yaml.FullLoader)
except FileNotFoundError as err:
	print(f"Message: Can`t find config - {settings.PATH_TO_RP_CONFIG}\nERROR: {err}")
	exit(1)
