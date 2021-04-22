from sqlalchemy import text

from .main import db
from .utils import error_handler


def get_job_type(email):
	query = f"select get_job_type({email});"

	response = error_handler(query)

	if response['success']:
		job_type = None
		for row in response['data']:
			job_type = str(row[0])

		return {'data': job_type, 'success': True}

	return response


def get_customer_flights(email):
	query = f"select get_customer_flights('{email}');"

	response = error_handler(query)

	if response['success']:
		data = list()
		for row in response['data']:
			cols = (row[0][1:-1]).split(sep=",")
			data.append(cols)

		return{'data': data, 'success': True}

	return response
		

