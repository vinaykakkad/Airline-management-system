from flask import current_app as app
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user

from ..connection.utils import get_table_info_records, book_ticket, cancel_ticket
from ..connection.functions import get_customer_flights, filter_flights, filter_history

@app.route('/passenger')
def passenger_home_route():
	print('here')
	return render_template('passenger/home.html')

@app.route('/check_history', methods=['POST', 'GET'])
def check_history_route():
	if request.method == 'GET':
		response = get_customer_flights(current_user.id)

		if not response['success']:
			flash(f"{response['data']}", 'error')
			return redirect(url_for('passenger_home_route'))

		context = {'data': response['data']}
		print('here', (response['data']))
		return render_template('passenger/view_tickets.html', **(context))


@app.route('/book_tickets', methods=['GET', 'POST'])
def book_tickets_route():
	if request.method == 'GET':
		response = get_table_info_records('flight')

		if not response['success']:
			return render_template('base/error.html')

		context = {
			'table_name': 'flight',
			'column_data': response['data']['column_data'],
			'records': response['data']['records']
		}
		return render_template('passenger/book_flight.html', **(context))

	if request.method == 'POST':
		source = request.form['source']
		destination = request.form['destination']
		code = request.form['code']
		t_class = request.form['class']
		travelling_date = request.form['travelling_date']
		seat = request.form['seat']

		response = book_ticket(current_user.id, source, destination, t_class, 
						travelling_date, seat, code)

		if response['success']:
			flash('Ticket booked successfully', 'success')
		else:
			flash(str(response['data']), 'error')

		return redirect(url_for('book_tickets_route'))


@app.route('/book_flight/filter')
def booking_filter():
	source = request.args.get('source')
	destination = request.args.get('destination')

	response = filter_flights(source, destination)

	print(response['data'])
	if not response['success']:
		return render_template('base/error.html')

	context = {
		'table_name': 'flight',
		'column_data': response['data']['column_data'],
		'records': response['data']['records']
	}
	return render_template('passenger/book_flight.html', **(context))


@app.route('/check_history/<filter>')
def check_history_filter(filter):
	response = 	filter_history(current_user.id, filter)

	if not response['success']:
		flash(f"{response['data']}", 'error')
		return redirect(url_for('passenger_home_route'))

	context = {'data': response['data']}
	return render_template('passenger/view_tickets.html', **(context))


@app.route('/cance_ticket', methods=['POST'])
def cancel_ticket_route():
	ticket_number = request.form['ticket_number']

	response = cancel_ticket(ticket_number)

	if not response['success']:
		flash(f"{response['data']}", 'error')
		return redirect(url_for('check_history_route'))

	return redirect(url_for('check_history_filter', filter='upcoming'))	