from flask import current_app as app
from flask import render_template, request, redirect, url_for, flash

from ..connection.utils import count_instances


@app.route('/passenger')
def employee_home_route():
	tables = [ 
		{'table': 'Flight', 'name': 'Flights'},
		{'table': 'Passenger', 'name': 'Passengers'},
		{'table': 'Ticket', 'name': 'Tickets'},
		{'table': 'Price', 'name': 'Prices'}
	]

	for table in tables:
		response =  count_instances(table['table'])

		if not response['success']:
			return render_template('base/error.html')
			
		table['instances'] = response['data']
		
	context = {'tables': tables}
	return render_template('passenger/home.html', **(context))