from sqlalchemy import text
from sqlalchemy.orm import query

from .main import db
from .utils import error_handler, get_table_info


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
		

def filter_flights(source, destination):
	column_data = get_table_info('flight')

	records = list()
	query = f"SELECT * FROM filter_flight('{source}', '{destination}');"
	result = error_handler(query)
	
	if result['success']:
		for row in result['data']:
			new_record = dict()
			
			for (column, record) in zip(column_data['data'], row):
				new_record[column['column_name']] = record

			records.append(new_record)

		return {
			'data': {
				'column_data': column_data['data'], 
				'records': records
			},
			'success': True
		}

	return result

def filter_history(email, filter):
	query = f"select flight_history_filter('{email}', '{filter}');"

	response = error_handler(query)

	if response['success']:
		data = list()
		for row in response['data']:
			cols = (row[0][1:-1]).split(sep=",")
			data.append(cols)

		return{'data': data, 'success': True}

	return response