from flask import current_app as app
from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user

from ..connection.utils import add_account, select_particulat_record
from .login_utils import User

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

	where_condition = f"email='{email}'"
	response = select_particulat_record('account', where_condition)

	if not response['success']:
		flash(str(response['data']), 'error')
		return redirect(url_for('login_page_route'))

	type, db_password = None, None
	for row in response['data']:
		type, db_password = row[2], row[1]

	if check_password_hash(db_password, password):
		user = User()
		user.id, user.type = email, type

		login_user(user)		

		flash('Logged in successfully', 'success')
		return redirect(url_for('home_page_view'))

	flash('Authentication Unsuccessful', 'error')
	return redirect(url_for('login_page_route'))


@app.route('/logout')
def logoute_route():
	logout_user()

	flash('Logged out successfully', 'success')
	return redirect(url_for('home_page_view'))