from flask.helpers import url_for
from ..connection.functions import get_job_type
from flask_login import current_user
from flask import redirect, flash


admin_modify = ['country', 'airport', 'airline', 'contains', 'employee',
                'flight', 'airport_authority', 'administration', 'engineer',
                'traffic_monitor', 'salary']

engineer_modify = ['flight']

airport_autority_mody = ['flight', 'price']

traffic_monitor_modify = ['flight', 'ticket']

administration_modify = ['passenger', 'ticket']

employee_view = ['flight', 'price', 'passenger', 'ticket']


def has_view_permission(table_name):
    if not current_user.is_authenticated:
        flash('You need to log in!!', 'error')
        return redirect(url_for('login_page_roure'))

    if current_user.type == 'passenger':
        if str(table_name).lower() != 'flight':
            flash('You do not have access to view this data!!', 'error')
            return redirect(url_for('passenger_home_route'))

    if current_user.type == 'employee':
        if str(table_name).lower() not in employee_view:
            flash('You do not have access to view this data!!', 'error')
            return redirect(url_for('employee_home_route'))

    return True


def has_modify_permission(table_name):
    if not current_user.is_authenticated:
        flash('You need to log in!!', 'error')
        return redirect(url_for('login_page_roure'))

    if current_user.type == 'passenger':
        if str(table_name).lower() != 'ticket':
            flash('You do not have access to modify this data!!', 'error')
            return redirect(url_for('passenger_home_route'))

    if current_user.type == 'employee':
        response = get_job_type(current_user.id)

        if not response['success']:
            flash('There was some error, try again!!', 'error')
            return redirect(url_for('employee_home_route'))

        job_type = response['data']

        if job_type == 'Administration':
            if str(table_name).lower() not in administration_modify:
                flash('You do not have access to modify this data!!', 'error')
                return redirect(url_for('employee_home_route'))

        if job_type == 'Engineer':
            if str(table_name).lower() not in engineer_modify:
                flash('You do not have access to modify this data!!', 'error')
                return redirect(url_for('employee_home_route'))

        if job_type == 'Traffic_monitor':
            if str(table_name).lower() not in traffic_monitor_modify:
                flash('You do not have access to modify this data!!', 'error')
                return redirect(url_for('employee_home_route'))

        else:
            if str(table_name).lower() not in airport_autority_mody:
                flash('You do not have access to modify this data!!', 'error')
                return redirect(url_for('employee_home_route'))

    if current_user.type == 'admin':
        if str(table_name).lower() not in admin_modify:
            flash('You do not have access to modify this data!!', 'error')
            return redirect(url_for('admin_home_route'))

    return True


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
        is_int = bool(column['data_type'] == 'integer')

        key = column['column_name']
        value = str(data[record]) if is_int else f"'{str(data[record])}'"

        if(len(str(data[record])) == 0):
            value = 'NULL'

        final = f"{key}={value}" if is_set else value

        values = f"{values}, {final}"

    return values[2:]
