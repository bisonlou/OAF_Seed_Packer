from os import environ
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def create_db(app, database_uri):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = app
    db.init_app(app)

    db.create_all()
    migrate = Migrate(app, db)


import api.models.farmer
import api.models.product
import api.models.order
import api.models.order_detail
