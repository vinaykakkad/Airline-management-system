from decouple import config
from flask import Flask, request, jsonify, render_template, redirect, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object(config('APP_SETTINGS'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route("/")
def home_page_view():
    return render_template('home/home.html')


@app.route("/login")
def login_page_view():
    return render_template('auth/login.html')


@app.route("/register")
def register_page_view():
    return render_template('auth/register.html')


if __name__ == '__main__':
    app.run()