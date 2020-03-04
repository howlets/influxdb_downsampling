import rp_generator.settings as settings


def check_env_variables():
	print(f"PATH_TO_RP_CONFIG={settings.PATH_TO_RP_CONFIG}")
	print(f"INFLUXDB_URL={settings.INFLUXDB_URL}")
	print(f"INFLUXDB_USER={settings.INFLUXDB_USER}")
	print(f"INFLUXDB_PASS={settings.INFLUXDB_PASS}")
