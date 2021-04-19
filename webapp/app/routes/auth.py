from flask import current_app as app
from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash

from ..connection.utils import add_account


@app.route('/register', methods=['GET', 'POST'])
def register_page_route():
	if request.method == 'GET':
		return render_template('auth/register.html')

	email, type = request.form['email'], request.form['type']
	password = generate_password_hash(request.form['password'])

	response = add_account(email, password, type)

	if response['success']:
		flash('Accound registered successfully', 'success')
	else:
		flash(str(response['data']), 'error')

	return redirect(url_for('home_page_view'))


@app.route('/login', methods=['GET', 'POST'])
def login_page_route():
	if request.method == 'GET':
		return render_template('auth/login.html')

	email, password = request.form['email'], request.form['password']
