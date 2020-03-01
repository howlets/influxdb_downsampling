from logger.logging import service_logger
from influxdb import InfluxDBClient
from urllib.parse import urlparse
import traceback
import rp_generator.settings as settings
import json

log = service_logger()


def _influx_client():
    influx_host = urlparse(settings.INFLUXDB_URL).hostname
    influx_port = urlparse(settings.INFLUXDB_URL).port

    client = InfluxDBClient(influx_host, influx_port, settings.INFLUXDB_USER, settings.INFLUXDB_PASS)

    return client


def get_influx_dbs():
    """Instantiate a connection to the InfluxDB."""
    dbs_list = []
    db_exclude = ['_internal']
    dbs = _influx_client().get_list_database()

    for db in dbs:
        if db['name'] not in db_exclude:
            dbs_list.append(db['name'])

    return dbs_list


def get_measurements(db_name):
    measurements = [measurement_list for measurement_list in _influx_client().query("SHOW MEASUREMENTS", database=db_name)]
    if measurements:
        return measurements[0]
    else:
        return []


def show_field_keys(measurement, db_name):
    value_list = []
    select_value_list = []
    query = f""" SHOW FIELD KEYS ON "{db_name}" FROM "{measurement}" """

    field_keys = [values for values in _influx_client().query(query, database=db_name)][0]

    for field in field_keys:
        value_list.append(field['fieldKey'])

    for single_value in list(set(value_list)):
        select_value_list.append(f"""mean("{single_value}") as "{single_value}" """)

    return ", ".join(select_value_list)


def _create_cq(rp_name, rp_settings, db_name, previous_rp):
    measurement_list = get_measurements(db_name)
    group_by = rp_settings.split("_")[1]

    for measurement in measurement_list:
        select_values = show_field_keys(measurement['name'], db_name)
        cq_name = f"cq_{rp_name}_{measurement['name']}"
        query_create = f"""
        CREATE CONTINUOUS QUERY "{cq_name}" ON "{db_name}"
        BEGIN
        SELECT {select_values} INTO "{db_name}"."{rp_name}"."{measurement['name']}" FROM {db_name}."{previous_rp}"."{measurement['name']}" GROUP BY time({group_by}), *
        END """

        log.info(f"rp_name: {rp_name}, query_create: {query_create}, previous_rp: {previous_rp}")

        try:
            _influx_client().query(query_create, database=db_name)
        except Exception:
            try:
                query_drop = f""" DROP CONTINUOUS QUERY {cq_name} ON "{db_name}" """
                _influx_client().query(query_drop, database=db_name)
                _influx_client().query(query_create, database=db_name)
                log.info(f"Drop CQ: cq_{rp_name}_{measurement['name']} for db:{db_name}")
            except Exception as err:
                log.error(msg=f"Can`t create RP: {err}")
                continue

        log.info(f"Create CQ: cq_{rp_name}_{measurement['name']} for db:{db_name}")


def generate_rps():
    dbs_list = get_influx_dbs()

    for db_name in dbs_list:
        previous_rp = settings.INFLUXDB_DEFAULT_POLICY
        for rp_name, rp_settings in json.loads(settings.INFLUXDB_RP).items():
            if rp_name != settings.INFLUXDB_DEFAULT_POLICY:
                try:
                    rp_duration = rp_settings.split("_")[0]
                    log.info(f"Create rp: {rp_name} for db: {db_name}")
                    _influx_client().create_retention_policy(rp_name, rp_duration, 1, database=db_name)
                    _create_cq(rp_name, rp_settings, db_name, previous_rp)
                    previous_rp = rp_name
                except Exception as err:
                    log.error(f"Can`t generate generate_rps. ERROR: {err}. Stack: {traceback.format_exc()}")
                    continue
