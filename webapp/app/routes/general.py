from flask import current_app as app
from flask import render_template, request

from ..connection.main import trial_insert

@app.route("/")
def home_page_view():
    return render_template('home/home.html')


@app.route("/login")
def login_page_view():
    return render_template('auth/login.html')


@app.route("/register")
def register_page_view():
    return render_template('auth/register.html')


@app.route("/test")
def test_route():
    city = request.args.get('city')
    state = request.args.get('state')
    country = request.args.get('country')

    result = trial_insert(city, state, country)
    return str(result)