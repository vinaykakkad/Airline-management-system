from flask_login import LoginManager, UserMixin
from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import check_password_hash

from ..connection.utils import select_particulat_record

login_manager = LoginManager()
login_manager.init_app(app)

def check_password(email, password):
	where_condition = f"email='{email}'"
	response = select_particulat_record('account', where_condition)

	if not response['success']:
		return False

	db_password = None
	for row in response['data']:
		db_password = row[1]

	return check_password_hash(db_password, password)


class User(UserMixin):
	pass


@login_manager.user_loader
def user_loader(email):
	where_condition = f"email='{email}'"
	response = select_particulat_record('account', where_condition)

	if not response['success']:
		return

	type = None
	for row in response['data']:
		type = row[2]

	user = User()
	user.id = email
	user.type = type 

	return user


@login_manager.request_loader
def request_loader(request):
	if request.method == 'POST':
		email = request.form.get('email')
		form_pass = request.form.get('password')

		where_condition = f"email='{email}'"
		response = select_particulat_record('account', where_condition)

		if not response['success']:
			return

		type = None
		for row in response['data']:
			type = row[2]

		user = User()
		user.id = email
		user.type = type

		user.is_authenticated = check_password(email, form_pass)

		return user