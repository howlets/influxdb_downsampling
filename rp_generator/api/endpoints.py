from rp_generator.api.restplus import api
from flask import request
from flask_restplus import Resource
from logger.logging import service_logger

log = service_logger()
ns = api.namespace('influx', description='InfluxDB Retention Generator')


@ns.route('/health')
class Health(Resource):

    @staticmethod
    def get():
        """
        Service health check
        """

        return {'status': 'UP'}, 200
