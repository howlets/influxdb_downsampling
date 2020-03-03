import rp_generator.settings as settings
from rp_generator.influx_worker.query_modifier import main_query_changer
import requests
from flask import request
from flask import Response
import json


class HandleRequest(object):
	def __init__(self, query_parameters, path):
		self.query_parameters = query_parameters
		self.path = path
		self.default_rps = settings.RP_CONFIG['default_rp']['name']

	@staticmethod
	def handle_result(content):
		result = json.loads(content.decode())['results'][0]
		if 'error' not in result:
			return True
		else:
			return False

	def process_influx(self):
		headers = request.headers
		cookies = request.cookies
		print(f"Query to Influx: {self.query_parameters}")
		r = requests.get(
			url=settings.INFLUXDB_URL + '/' + self.path,
			params=self.query_parameters,
			headers=headers,
			cookies=cookies,
			stream=True
		)

		print(f"Content: {r.content}: InfluxQuery: {self.query_parameters}")
		excluded_headers = ['content-length', 'server', 'content-encoding']
		headers = [(name, value) for (name, value) in r.raw.headers.items() if name.lower() not in excluded_headers]
		response = Response(r.content, r.status_code, headers)

		return response, r.content

	def get_data_from_influx(self, rp_name=None):
		if rp_name is None:
			self.query_parameters['q'] = main_query_changer(query=self.query_parameters['q'])
		else:
			self.query_parameters['q'] = main_query_changer(query=self.query_parameters['q'], rp_name=rp_name)

		response, content = self.process_influx()

		if self.handle_result(content=content):
			return response

	def process(self):
		response = self.get_data_from_influx()
		if response is not None:
			return response
		else:
			for default_rp in self.default_rps:
				response = self.get_data_from_influx(rp_name=default_rp)

				if response is not None:
					return response

			return response
