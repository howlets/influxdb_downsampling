import time
from rp_generator.settings import RP_CONFIG


def _modify_query(query, rp_name):
    current_rp = query.split("FROM ")[1].split(" ")[0]

    if len(current_rp.split(".")) >= 2:
        measurement = current_rp.split(".")[1]

        modified_rp = f""""{rp_name}".{measurement}"""
    else:
        modified_rp = f""""{rp_name}".{current_rp}"""

    new_query = query.replace(current_rp, modified_rp, 1)

    return new_query


def days_to_seconds(time_in_days):
    duration_in_sec = int(time_in_days.replace('d', '')) * 86400

    return duration_in_sec


def _identify_rp(time_range):
    if time_range < days_to_seconds(RP_CONFIG['default_rp']['duration']):
        return RP_CONFIG['default_rp']['name']

    for custom_rp in RP_CONFIG['custom_rp']:
        if time_range < int(days_to_seconds(custom_rp['duration'])):
            return custom_rp['name']


def _process_dynamic_time(query):
    current_milli_time = int(round(time.time() * 1000))
    time_from_now = query.split("ms")[0]
    time_diff = round((int(current_milli_time) - int(time_from_now)) / 1000)

    return _identify_rp(time_diff)


def _process_static_time(query):
    seconds_per_unit = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}
    time_from_now = query.split(" ")[2]
    time_in_seconds = int(time_from_now[:-1]) * seconds_per_unit[time_from_now[-1]]

    return _identify_rp(time_in_seconds)


def main_query_changer(query, rp_name=None):
    if 'SHOW RETENTION POLICIES' in query:
        return query

    if 'SHOW TAG VALUES' in query:
        modified_query = _modify_query(query=query, rp_name='default')

        return modified_query

    if rp_name:
        modified_query = _modify_query(query=query, rp_name=rp_name)

        return modified_query
    else:
        split_query = query.split("time >= ")[1]
        if split_query.startswith("now()"):
            rp_name = _process_static_time(split_query)
        else:
            rp_name = _process_dynamic_time(split_query)

        modified_query = _modify_query(query=query, rp_name=rp_name)

        return modified_query

