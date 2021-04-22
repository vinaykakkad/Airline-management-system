import csv

from flask import current_app as app
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user
from flask.globals import g
from werkzeug.security import generate_password_hash, check_password_hash

from .login_utils import User
from .utils import (has_view_permission, create_values, create_where_condition,
                    has_modify_permission)
from ..connection.utils import (get_table_info, add_record, delete_record,
                                get_table_info_records, select_particulat_record, add_account,
                                update_record)


@app.route("/")
def home_page_view():
    return render_template('home/home.html')


@app.route('/view/<table_name>')
def view_table_route(table_name):
    result = has_view_permission(table_name)

    if result != True:
        return result

    response = get_table_info_records(table_name)

    if not response['success']:
        return render_template('base/error.html')

    context = {
        'table_name': table_name,
        'column_data': response['data']['column_data'],
        'records': response['data']['records']
    }
    return render_template('table/tables.html', **(context))


@app.route('/admin/delete', methods=['POST'])
def delete_record_route():
    table_name = request.form.get('table_name')
    result = has_modify_permission(table_name)

    if result != True:
        return result

    record = request.form.get('record')
    where_condition = create_where_condition(record)
    response = delete_record(table_name, where_condition)

    if response['success']:
        flash('Record deleted successfully', 'success')
    else:
        flash(str(response['data']), 'error')

    return redirect(url_for('view_table_route', table_name=table_name))


@app.route('/admin/add/<table_name>', methods=['POST'])
def add_record_route(table_name):
    result = has_modify_permission(table_name)

    if result != True:
        return result

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

    return redirect(url_for('view_table_route', table_name=table_name))


@app.route('/admin/update/<table_name>', methods=['POST'])
def update_record_route(table_name):
    result = has_modify_permission(table_name)

    if result != True:
        return result

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

    return redirect(url_for('view_table_route', table_name=table_name))


@app.route('/register', methods=['GET', 'POST'])
def register_page_route():
    # if current_user.is_authenticated:
    #     flash('You are already logged in!!', 'success')
    #     return redirect(url_for('home_page_view'))

    if request.method == 'GET':
        return render_template('auth/register.html')

    email, type = request.form['email'], request.form['type']
    password = generate_password_hash(request.form['password'])

    response = add_account(email, password, type)

    if response['success']:
        flash('Account registered successfully', 'success')
        user = User()
        user.id, user.type = email, type

        login_user(user)
    else:
        flash(str(response['data']), 'error')

    return redirect(url_for('home_page_view'))


@app.route('/login', methods=['GET', 'POST'])
def login_page_route():
    # if current_user.is_authenticated:
    #     flash('You are already logged in!!', 'success')
    #     return redirect(url_for('home_page_view'))

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
def logout_route():
    logout_user()

    flash('Logged out successfully', 'success')
    return redirect(url_for('home_page_view'))


# *********************** TESTING ********************************

@app.route("/test")
def testing_route():
    # email = 'vinay.k@ahduni.edu.in'
    # form_pass = 'vinay'

    # where_condition = f"email='{email}'"
    # response = select_particulat_record('account', where_condition)

    # print(response)
    # if not response['success']:
    # 	return

    # type, password = None, None
    # for row in response['data']:
    # 	print('HERE', row)
    # 	type, password = row[2], row[1]

    return f"{current_user.id}, {current_user.type}, {current_user.is_authenticated}"


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
                print('here', str(col), col_info['column_name'], col_info['data_type'])
                if (col_info['data_type'] == 'integer'):
                    values = f"{values}, {str(col)}"
                else:
                    values = f"{values}, '{str(col)}'"

            temp = add_record(table_name, values[2:])
            print(temp['data'])

    return 'done' if temp['success'] else 'not done'