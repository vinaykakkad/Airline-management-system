# from flask import Flask, request, jsonify, render_template, redirect, flash
# from flask_sqlalchemy import SQLAlchemy


# db = SQLAlchemy(app)


from app.config import create_app

app = create_app()


if __name__ == "__main__":
    app.run()