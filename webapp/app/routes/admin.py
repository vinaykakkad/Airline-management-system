from flask import current_app as app
from flask import render_template, request, redirect, url_for, flash

from .utils import create_values, create_where_condition
from ..connection.utils import (count_instances, get_table_info, delete_record,
                                add_record, get_table_info_records, update_record)


@app.route('/admin')
def admin_home_route():
    tables = [
        {'table': 'Country', 'name': 'Countries'},
        {'table': 'Airport', 'name': 'Airports'},
        {'table': 'Airline', 'name': 'Airlines'},
        {'table': 'Contains', 'name': 'Connections'},
        {'table': 'Employee', 'name': 'Employees'},
        {'table': 'Airport_authority', 'name': 'Airport Authorities'},
        {'table': 'Engineer', 'name': 'Engineers'},
        {'table': 'Traffic_monitor', 'name': 'Traffic Monitors'},
        {'table': 'Administration', 'name': 'Administrators'},
        {'table': 'Salary', 'name': 'Salary Types'},
    ]

    for table in tables:
        response = count_instances(table['table'])

        if not response['success']:
            return render_template('base/error.html')

        table['instances'] = response['data']

    context = {'tables': tables}
    return render_template('admin/home.html', **(context))
