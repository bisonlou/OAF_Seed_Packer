import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from api.database import create_db
from api.controllers.errors import errorhandler_app
from api.controllers.farmers import farmers_app
from api.controllers.orders import orders_app
from api.controllers.products import products_app

app = Flask(__name__)

if os.environ["FLASK_ENV"] == "testing":
    database_path = os.environ["TEST_DATABASE_URL"]
else:
    database_path = os.environ["DATABASE_URL"]

create_db(app, database_path)

CORS(app, resources={r"/*": {"origins": "*"}})


@app.after_request
def after_request(response):
    """ configuring CORS"""
    response.headers.add(
        "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
    )
    response.headers.add(
        "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
    )
    return response


@app.route("/")
def index():
    return "Welcome to OAF seed packer!"


errorhandler_app(app)
farmers_app(app)
products_app(app)
orders_app(app)
