from flask import current_app as app
from flask import render_template, request, redirect, url_for, flash

from ..connection.utils import (count_instances, get_table_info, delete_record,
								add_record, get_table_info_records, update_record)	


def create_where_condition(data):
	conditions = data.split(',')
	
	counter = 0
	where_condition = str()

	for condition in conditions:
		counter += 1
		where_condition = where_condition + condition

		if(counter == len(conditions) - 1):
			break
		else:
			where_condition = where_condition + ' AND '

	return where_condition


def create_values(column_data, data, is_set):
	values = str()

	for column, record in zip(column_data, data):
		is_int = bool(column['data_type']=='integer')

		key = column['column_name']
		value = str(data[record]) if is_int else f"'{str(data[record])}'"

		if(len(str(data[record])) == 0):
			value = 'NULL'
			
		final = f"{key}={value}" if is_set else value

		values = f"{values}, {final}"
	
	return values[2:]


@app.route('/admin')
def admin_home_page_view():
	tables = [ 
		{'table': 'Country', 'name': 'Countries', 'instances': 0},
		{'table': 'Airport', 'name': 'Airports', 'instances': 0},
		{'table': 'Airline', 'name': 'Airlines', 'instances': 0},
		{'table': 'Contains', 'name': 'Connections', 'instances': 0},
		{'table': 'Employee', 'name': 'Employees', 'instances': 0},
		{'table': 'Airport_authority', 'name': 'Airport Authorities', 'instances': 0},
		{'table': 'Engineer', 'name': 'Engineers', 'instances': 0},
		{'table': 'Traffic_monitor', 'name': 'Traffic Monitors', 'instances': 0},
		{'table': 'Administration', 'name': 'Administrators', 'instances': 0},
		{'table': 'Salary', 'name': 'Salary Types', 'instances': 0},
	]

	for table in tables:
		response =  count_instances(table['table'])

		if not response['success']:
			return render_template('base/error.html')
			
		table['instances'] = response['data']
		
	context = {'tables': tables}
	return render_template('admin/home.html', **(context))


@app.route('/admin/<table_name>')
def admin_table_routes(table_name):
	response = get_table_info_records(table_name)

	if not response['success']:
		return render_template('base/error.html')

	context = {
		'table_name' : table_name,
		'column_data': response['data']['column_data'],
		'records': response['data']['records']	
	}
	return render_template('admin/tables.html', **(context))


@app.route('/admin/delete', methods=['POST'])
def admin_delete_route():
	record = request.form.get('record')
	table_name = request.form.get('table_name')

	where_condition = create_where_condition(record)
	
	response = delete_record(table_name, where_condition)

	if response['success']:
		flash('Record deleted successfully', 'success')
	else:
		flash(str(response['data']), 'error')

	return redirect(url_for('admin_table_routes', table_name=table_name))


@app.route('/admin/add/<table_name>', methods=['POST'])
def admin_add_route(table_name):
	data = request.form
	column_data = get_table_info(table_name)
	
	if not column_data['success']:
		return render_template('base/error.html')

	values = create_values(column_data['data'], data, False)
			
	response = add_record(table_name, values)

	if response['success']:
		flash('Record added successfully', 'success')
	else:
		flash(str(response['data']), 'error')

	return redirect(url_for('admin_table_routes', table_name=table_name))


@app.route('/admin/update/<table_name>', methods=['POST'])
def admin_update_route(table_name):
	data = request.form.to_dict()
	where_data = data.pop('where-condition')
	column_data = get_table_info(table_name)

	if not column_data['success']:
		return render_template('base/error.html')

	where_condition = create_where_condition(where_data)
	values = create_values(column_data['data'], data, True)

	response = update_record(table_name, values, where_condition)

	if response['success']:
		flash('Record updated successfully', 'success')
	else:
		flash(str(response['data']), 'error')

	return redirect(url_for('admin_table_routes', table_name=table_name))