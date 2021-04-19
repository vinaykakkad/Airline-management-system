import csv, os

from flask import current_app as app
from flask import render_template, request

from ..connection.utils import get_table_info, add_record, select_particulat_record

@app.route("/")
def home_page_view():
	return render_template('home/home.html')

@app.route("/test")
def testing_route():
	email = 'vinay.k@ahduni.edu.in'
	form_pass = 'vinay'

	where_condition = f"email='{email}'"
	response = select_particulat_record('account', where_condition)

	print(response)
	if not response['success']:
		return

	type, password = None, None
	for row in response['data']:
		print('HERE', row)
		type, password = row[2], row[1]

	return {1: type, 2: password}

@app.route("/temp_add/<table_name>")
def test_route(table_name):
	print(str(table_name).lower())
	result = get_table_info(str(table_name).lower())

	if not result['success']:
		return 'there was some error in the table_name'

	with open(f'csvs/{table_name}.csv', encoding="utf-8-sig") as file:
		reader = csv.reader(file, delimiter=',')

		for row in reader:
			values = str()

			for col, col_info in zip(row, result['data']):
				if (col_info['data_type'] == 'integer'):
					values = f"{values}, {str(col)}"
				else:
					values = f"{values}, '{col}'"

			temp = add_record(table_name, values[2:])
			print(temp['data'])        

	return 'done' if temp['success'] else 'not done'