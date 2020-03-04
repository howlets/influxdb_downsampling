from logger.logging import service_logger
from influxdb import InfluxDBClient
from urllib.parse import urlparse
import traceback
import rp_generator.settings as settings
import time
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
    while True:
        try:
            dbs = _influx_client().get_list_database()
            break
        except Exception as err:
            print(f"Can`t connect to InfluxDB: {settings.INFLUXDB_URL} \nRetry in 10 seconds")
            time.sleep(10)
            continue

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
        if field['fieldType'] != 'string':
            value_list.append(field['fieldKey'])

    for single_value in list(set(value_list)):
        select_value_list.append(f"""mean("{single_value}") as "{single_value}" """)

    return ", ".join(select_value_list)


def _create_cq(rp_name, aggr_period, db_name, previous_rp):
    measurement_list = get_measurements(db_name)

    for measurement in measurement_list:
        select_values = show_field_keys(measurement['name'], db_name)
        print(select_values)
        cq_name = f"cq_{rp_name}_{measurement['name']}"
        query_create = f"""
        CREATE CONTINUOUS QUERY "{cq_name}" ON "{db_name}"
        BEGIN
        SELECT {select_values} INTO "{db_name}"."{rp_name}"."{measurement['name']}" FROM {db_name}."{previous_rp}"."{measurement['name']}" GROUP BY time({aggr_period}), *
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


def days_to_hours(time_in_days):
    duration_in_hours = int(time_in_days.replace('d', '')) * 24

    return f'{duration_in_hours}h0m0s'


def check_default_rp_duration(db_name):
    rp_list = _influx_client().get_list_retention_policies(database=db_name)

    for rp in rp_list:
        if rp['name'] == settings.RP_CONFIG['default_rp']['name']:
            if rp['duration'] != days_to_hours(settings.RP_CONFIG['default_rp']['duration']):
                modify_default_rp = _influx_client().alter_retention_policy(
                    name=rp['name'],
                    database=db_name,
                    duration=settings.RP_CONFIG['default_rp']['duration'],
                    default=True
                )
                print(f"Duration of default RP: {rp['name']} has been changed to {settings.RP_CONFIG['default_rp']['duration']}\nResult: {modify_default_rp}")


def generate_rps():
    # TODO: Alter duration of RP if it was changed in Conf file
    dbs_list = get_influx_dbs()

    for db_name in dbs_list:
        check_default_rp_duration(db_name)
        previous_rp = settings.RP_CONFIG['default_rp']['name']
        for custom_rp in settings.RP_CONFIG['custom_rp']:
            if custom_rp['name'] != settings.RP_CONFIG['default_rp']['name']:
                try:
                    log.info(f"Create rp: {custom_rp['name']} for db: {db_name}")
                    _influx_client().create_retention_policy(custom_rp['name'], custom_rp['duration'], 1, database=db_name)
                    _create_cq(custom_rp['name'], custom_rp['aggregation'], db_name, previous_rp)
                    previous_rp = custom_rp['name']
                except Exception as err:
                    log.error(f"Can`t generate generate_rps. ERROR: {err}. Stack: {traceback.format_exc()}")
                    continue
