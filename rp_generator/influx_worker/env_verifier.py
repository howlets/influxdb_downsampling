import rp_generator.settings as settings
from logger.logging import service_logger

log = service_logger()


def check_env_variables():
	log.info(msg=f"PATH_TO_RP_CONFIG={settings.PATH_TO_RP_CONFIG}")
	log.info(msg=f"LOG_LEVEL={settings.LOG_LEVEL}")
	log.info(msg=f"LOG_PATH={settings.LOG_PATH}")
	log.info(msg=f"INFLUXDB_URL={settings.INFLUXDB_URL}")
	log.info(msg=f"INFLUXDB_USER={settings.INFLUXDB_USER}")
	log.info(msg=f"INFLUXDB_PASS={settings.INFLUXDB_PASS}")
