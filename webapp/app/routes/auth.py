from flask import current_app as app
from flask import render_template, request, redirect, url_for



@app.route('/login', methods=['GET', 'POST'])
def login_page_route():
	if request.method == 'GET':
		return render_template('auth/loign.html')

	email, password = request.form['email'], request.form['password']


	