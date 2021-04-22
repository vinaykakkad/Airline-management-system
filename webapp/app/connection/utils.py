from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from .main import db


def error_handler(query):
	result = {'data': None, 'success': True}
	
	try:
		result['data'] = db.engine.execute(query)
	except SQLAlchemyError as e:
		result['success'] = False
		result['data'] = str(e.orig)

	return result

		
def count_instances(table_name):
	table_name = str(table_name).lower()

	query = f'SELECT COUNT(*) FROM {table_name};'
	result = error_handler(query)
	
	if result['success']:
		count = 0

		for row in result['data']:
			count = row[0]

		return {'data': int(count), 'success': True}

	return result


def get_table_info(table_name):
	table_name = str(table_name).lower()


	query = f"""SELECT column_name, data_type FROM information_schema.columns 
				WHERE table_name='{table_name}' 
				ORDER BY ordinal_position;"""
	result = error_handler(query)

	if result['success']:
		column_data = []
	
		for row in result['data']:
			record = dict()
			record['column_name'], record['data_type'] = row[0], row[1]
			column_data.append(record)
			
		return {'data': column_data, 'success': True}

	return result


def get_table_info_records(table_name):
	table_name = str(table_name).lower()

	column_data = get_table_info(table_name)

	if column_data['success']:
		records = list()
		query = f'SELECT * FROM {table_name};'
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

	return column_data


def delete_record(table_name, where_condition):
	table_name = str(table_name).lower()

	query = f"DELETE FROM {table_name} WHERE ({where_condition});"

	return error_handler(query)
	

def add_record(table_name, values):
	table_name = str(table_name).lower()

	query = f"INSERT INTO {table_name} VALUES({values});"

	return error_handler(query)	


def update_record(table_name, set_values, where_condition):
	table_name = str(table_name).lower()

	query = f"UPDATE {table_name} SET {set_values} WHERE ({where_condition})"

	return error_handler(query)


def add_account(email, password, type):
	query_text = f"call add_account('{email}', '{password}', '{type}');"
	query = text(query_text).execution_options(autocommit=True)

	return error_handler(query)


def book_ticket(email, source, destination, t_class, date, seat, code):
	query_text = f"call book_ticket('{email}', '{source}', '{destination}', '{t_class}', '{date}', '{seat}', '{code}');"
	query = text(query_text).execution_options(autocommit=True)

	return error_handler(query)


def cancel_ticket(ticket_number):
	query_text = f"CALL cancel_ticket(CAST({int(ticket_number)} AS BIGINT));"
	query = text(query_text).execution_options(autocommit=True)

	return error_handler(query)


def select_particulat_record(table_name, where_condition):
	table_name = str(table_name).lower()

	query = f"SELECT * FROM {table_name} WHERE {where_condition};"

	return error_handler(query)