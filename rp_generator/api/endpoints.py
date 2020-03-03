from rp_generator.api.restplus import api
from flask_restplus import Resource
from logger.logging import service_logger
from rp_generator.influx_worker.proxy_handler import HandleRequest
from flask import request

log = service_logger()
ns = api.namespace('influx', description='InfluxDB Retention Generator')


@ns.route('/<path:path>')
class InfluxProxy(Resource):

    @staticmethod
    def get(path):
        params = dict(request.args)
        data = HandleRequest(query_parameters=params, path=path)
        response = data.process()

        return response


@ns.route('/health')
class Health(Resource):

    @staticmethod
    def get():
        """
        Service health check
        """

        return {'status': 'UP'}, 200
