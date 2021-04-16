from flask import current_app as app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy(app)

def trial_insert(city, state, country):
	query = text(f"INSERT INTO Country VALUES('{city}', '{state}', '{country}'); ")
	result = db.engine.execute(query)

	return result